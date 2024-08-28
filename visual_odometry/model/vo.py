import numpy as np
import cv2
from tqdm import tqdm

from model.features import FeatureDetectingAndMatching
from utils.utils import se3_from_rot_and_t

class VisualOdometry:

    def __init__(self, detect_method="ORB", match_method="BF"):

        cv2_methods = FeatureDetectingAndMatching(detect_method, match_method)
        self.detecter = cv2_methods.detecter
        self.matcher = cv2_methods.mathcher

    def filtered_keypoint(self, kp1, kp2, match_list, threshold=0.7):

        good_match_list = []
        try:
            for m, n in match_list:
                if m.distance < threshold * n.distance:
                    good_match_list.append(m)
        except:
            pass

        q1 = np.float32([kp1[m.queryIdx].pt for m in good_match_list])
        q2 = np.float32([kp2[m.trainIdx].pt for m in good_match_list])

        return q1, q2

    def epipolor_transformation(self, kp1, kp2, intrinsic, projection):
        essential, _ = cv2.findEssentialMat(kp1, kp2, intrinsic)
        rot1, rot2, t = cv2.decomposeEssentialMat(essential)
        t = t.flatten()
        possible_sol = [[rot1, t], [rot1, -t], [rot2, t], [rot2, -t]]

        # determine solution and compute relative scale
        sum_of_pos_depth_list = []
        relative_scale_list = []
        for rot, t in possible_sol:
            # relative transformation matrix between first and second image
            T = se3_from_rot_and_t(rot, t)
            # projection matrix of second image
            P = np.hstack((intrinsic, np.zeros((3, 1))))@T

            # reconstruct points (could be used for mapping)
            homo_kp1 = cv2.triangulatePoints(projection, P, kp1.T, kp2.T) # (4, n)
            homo_kp2 = T@homo_kp1 # (4, n)
            # de-homogenize
            dhomo_kp1 = (homo_kp1[:3, :]/homo_kp1[3, :]).T # (n, 3)
            dhomo_kp2 = (homo_kp2[:3, :]/homo_kp2[3, :]).T # (n, 3)

            # check which solution has the most positive depth (z-coordinate)
            sum_of_pos_depth = np.sum(dhomo_kp1[:, 2] > 0) + np.sum(dhomo_kp2[:, 2] > 0)
            sum_of_pos_depth_list.append(sum_of_pos_depth)

            # calculate relative scale by some edges between keypoints
            relative_scale = []
            num_edges = dhomo_kp1.shape[0] - 1
            for i in range(num_edges):
                edge1 = np.linalg.norm(dhomo_kp1[i+1] - dhomo_kp1[i])
                edge2 = np.linalg.norm(dhomo_kp2[i+1] - dhomo_kp2[i])
                if edge2 != 0.0:
                    relative_scale.append(edge1/edge2)
            relative_scale_list.append(sum(relative_scale)/len(relative_scale))

        rot, t = possible_sol[np.argmax(sum_of_pos_depth_list)]
        t *= relative_scale_list[np.argmax(sum_of_pos_depth_list)]

        return se3_from_rot_and_t(rot, t)


    def run(self, data):
        
        self.pred_path = []
        self.gt_path = []

        for i, gt_pose in enumerate(tqdm(data.poses, unit="pose", desc="Visual odometry")):

            if i == 0:
                abs_pose = gt_pose
                curr_keypoint, curr_descriptor = self.detecter.detectAndCompute(data.images[0], None)
            else:
                curr_keypoint, curr_descriptor = self.detecter.detectAndCompute(data.images[i], None)
                match_list = self.matcher.knnMatch(prev_descriptor, curr_descriptor, k=2)
                match_list = sorted(match_list, key=lambda x:x[0].distance)
            
                kp1, kp2 = self.filtered_keypoint(prev_keypoint, curr_keypoint, match_list)
                rel_pose = self.epipolor_transformation(kp1, kp2, data.intrinsic, data.projection)
                
                # the odometry model is P1@T=P2, update absolute pose by P2=P1@inv(T)
                abs_pose = abs_pose@np.linalg.inv(rel_pose)

                self.pred_path.append((abs_pose[0, 3], abs_pose[2, 3]))
                self.gt_path.append((gt_pose[0, 3], gt_pose[2, 3]))
            
            prev_keypoint = curr_keypoint
            prev_descriptor = curr_descriptor
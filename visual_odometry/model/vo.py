import numpy as np
import cv2
from tqdm import tqdm

from model.features import FeatureDetectingAndMatching
from utils.utils import se3_from_rot_and_t
from visualize.trajectory import plot_path

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
        # The transformation solved by essential matrix with OpenCV is by solving x2@E@x1=0.
        # The transformation solved by essential matrix derived by P1@T=P2 (T is the relative pose) is by solving x1@E@x2=0.
        # Therefore, we solve (x1@E@x2).T=x2@E.T@x1=0. Refer to Standford CS231A lecture notes for more details.
        essential, _ = cv2.findEssentialMat(kp1, kp2, intrinsic) 
        rot1, rot2, t = cv2.decomposeEssentialMat(essential.T) 
        t = t.flatten()
        possible_sol = [[rot1, t], [rot1, -t], [rot2, t], [rot2, -t]]

        # determine solution and compute relative scale
        sum_of_pos_depth_list = []
        rel_scale_list = []
        for rot, t in possible_sol:
            # Assume that the absolute pose of first image is identity, then the absolute pose of second image is T.
            # Note that the extrinsic matrix is the inverse of absoulute pose.
            # Projection matrix of first image is K@inv(I)=K, which is the camera's projection matrix.
            # Projection matrix of second image is K@inv(T).
            T = se3_from_rot_and_t(rot, t) 
            P = np.hstack((intrinsic, np.zeros((3, 1))))@np.linalg.inv(T) 

            # reconstruct points (could be used for mapping)
            homo_kp1 = cv2.triangulatePoints(projection, P, kp1.T, kp2.T) # (4, n)
            homo_kp2 = np.linalg.inv(T)@homo_kp1 # P1@T=P2 implies T@p2=p1
            # de-homogenize
            dhomo_kp1 = (homo_kp1[:3, :]/homo_kp1[3, :]).T # (n, 3)
            dhomo_kp2 = (homo_kp2[:3, :]/homo_kp2[3, :]).T 

            # check which solution has the most positive depth (z-coordinate)
            sum_of_pos_depth = np.sum(dhomo_kp1[:, 2] > 0) + np.sum(dhomo_kp2[:, 2] > 0)
            sum_of_pos_depth_list.append(sum_of_pos_depth)

            # calculate relative scale by some edges between keypoints
            rel_scale = []
            num_edges = dhomo_kp1.shape[0] - 1
            for i in range(num_edges):
                edge1 = np.linalg.norm(dhomo_kp1[i+1] - dhomo_kp1[i])
                edge2 = np.linalg.norm(dhomo_kp2[i+1] - dhomo_kp2[i])
                if edge2 != 0.0:
                    rel_scale.append(edge1/edge2)
            rel_scale_list.append(sum(rel_scale)/len(rel_scale))

        rot, t = possible_sol[np.argmax(sum_of_pos_depth_list)]
        t *= rel_scale_list[np.argmax(sum_of_pos_depth_list)]

        return se3_from_rot_and_t(rot, t)


    def run(self, data, plot_trajectory=True):
        # log result
        log_file = open("./result/{0:0=2d}.txt".format(data.sequence), "w")
        # visualize path
        if plot_trajectory:
            pred_path = []
            gt_path = []

        for i, image in enumerate(tqdm(data, unit="image", desc="Visual odometry")):

            gt_pose = data.poses[i]

            if i == 0:
                abs_pose = gt_pose
                curr_keypoint, curr_descriptor = self.detecter.detectAndCompute(image, None)
            else:
                curr_keypoint, curr_descriptor = self.detecter.detectAndCompute(image, None)
                match_list = self.matcher.knnMatch(prev_descriptor, curr_descriptor, k=2)
                match_list = sorted(match_list, key=lambda x:x[0].distance)
            
                kp1, kp2 = self.filtered_keypoint(prev_keypoint, curr_keypoint, match_list)
                rel_pose = self.epipolor_transformation(kp1, kp2, data.intrinsic, data.projection)
                
                # odometry 
                abs_pose = abs_pose@rel_pose

                if plot_trajectory: # (x, z)
                    pred_path.append((abs_pose[0, 3], abs_pose[2, 3])) 
                    gt_path.append((gt_pose[0, 3], gt_pose[2, 3]))

            # log poses (format) i T00 T01 T02 T03 T10 T11 T12 T13 T20 T21 T22 T23 
            vec_pose = abs_pose[:3, :4].flatten()
            n = log_file.write(str(i) + ' ' + ' '.join(map(str, vec_pose)) + '\n')

            prev_keypoint = curr_keypoint
            prev_descriptor = curr_descriptor

        log_file.close()

        if plot_trajectory:
            plot_path(pred_path, gt_path, data.sequence)
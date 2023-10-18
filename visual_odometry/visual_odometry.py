import matplotlib.pyplot as plt
import numpy as np
import cv2

from tqdm import tqdm
import os

class Plot:

    def __init__(self, images):

        self.images = images

    def put_text(self, image, position, text, color=(96,69,233), fontScale=0.7, thickness=1, font=cv2.FONT_HERSHEY_SIMPLEX):
        
        if not isinstance(position, tuple):
            (label_width, label_height), _ = cv2.getTextSize(text, font, fontScale, thickness)

            pos_h, pos_v = 0,0
            h, v, *_ = image.shape
            place_h, place_v = position.split("_")

            if place_h == "top": pos_h = label_height
            elif place_h == "bottom": pos_h = h
            elif place_h == "center": pos_h = h//2 + label_height//2

            if place_v == "left": pos_v = 0
            elif place_v == "right": pos_v = v - label_width
            elif place_v == "center": pos_v = v//2 - label_width//2

            position = (pos_v, pos_h)

        image = cv2.putText(image, text, position, font, fontScale, color, thickness, cv2.LINE_AA)

        return image

    def play_trip(self, timestamps=None, color_mode=False, waite_time=1, win_name="Trip"):

        frame_count = 0
        for i, img in enumerate(self.images):

            if not color_mode: img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            show_image = self.put_text(img, "top_right", f"Frame: {frame_count}/{len(self.images)}")

            if timestamps is not None:
                time = timestamps[i]
                show_image = self.put_text(show_image, "bottom_right", f"{time}")

            cv2.imshow(win_name, show_image)
            key = cv2.waitKey(waite_time)

            if key == 27: break # Esc
            frame_count += 1

        cv2.destroyWindow(win_name)
        for i in range(5): cv2.waitKey(1) ### Mac

    def save_paths(self, gt_path, pred_path, data, detect, match):

        gt_path = np.array(gt_path)
        pred_path = np.array(pred_path)

        err = np.linalg.norm(gt_path - pred_path, axis=1)

        save_dir = os.path.join("./results/{}/".format(data))
        if not os.path.exists(save_dir): os.makedirs(save_dir)

        plt.figure()
        plt.plot([x for x in pred_path[:, 0]], [z for z in pred_path[:, 1]], "b")  # x,z
        plt.plot([x for x in gt_path[:, 0]], [z for z in gt_path[:, 1]], "r")  # x,z
        plt.grid()
        plt.title("VO - Seq {}".format(data))
        plt.xlabel("Translation in x direction [m]")
        plt.ylabel("Translation in z direction [m]")
        plt.legend(["estimated", "ground truth"]);
        plt.savefig(os.path.join(save_dir + detect + "_" + match + "_path.png"))

        plt.figure()
        plt.plot(np.arange(len(err)),err)
        plt.grid()
        plt.title("VO - Seq {} error".format(data))
        plt.xlabel("Num of frame")
        plt.legend(["err"]);
        plt.savefig(os.path.join(save_dir + detect + "_" + match + "_error.png"))




class Visual_Odometry():
    
    def __init__(self, data_dir, detect_method, match_method, sample_scale):

        self.images = self.load_images(data_dir[0])
        self.instrinsic_matrix, self.projection_matrix = self.load_calib(data_dir[1])
        self.ground_truth_poses = self.load_poses(data_dir[2])
 
        self.detecter, self.matcher = self.detecter_and_matcher(detect_method, match_method)
        self.kp, self.des = self.detecter.detectAndCompute(self.images[0], None)
        self.sample_scale = sample_scale

        with open(data_dir[2]) as f: 
            self.annotations = f.readlines()

    @staticmethod
    def load_calib(filepath):

        with open(filepath, 'r') as f:
            params = np.fromstring(f.readline()[4:], dtype=np.float64, sep=' ') ### (P1: ) 4 elements
            P = np.reshape(params, (3, 4))
            K = P[0:3, 0:3]
        return K, P

    @staticmethod
    def load_poses(filepath):

        poses = []
        with open(filepath, 'r') as f:
            for line in f.readlines():
                T = np.fromstring(line, dtype=np.float64, sep=' ')
                T = np.vstack((T.reshape(3, 4), [0, 0, 0, 1]))
                poses.append(T)
        return poses

    @staticmethod
    def load_images(filepath):

        image_list = []
        for file in tqdm(sorted(os.listdir(filepath)), unit="image", desc="Loading Images"):
            image_path = os.path.join(filepath, file)
            image_list.append(cv2.imread(image_path, cv2.IMREAD_GRAYSCALE))
        return image_list

    @staticmethod
    def transformation_matrix(R, t):

        T = np.eye(4, dtype=np.float64)
        T[:3, :3] = R
        T[:3, 3] = t
        return T

    def get_scale_gt(self, i):

        pos_1 = self.annotations[i-1].strip().split()
        x_prev, y_prev, z_prev = float(pos_1[3]), float(pos_1[7]), float(pos_1[11])

        pos_2 = self.annotations[i].strip().split()
        x, y, z = float(pos_2[3]), float(pos_2[7]), float(pos_2[11])

        return np.sqrt((x - x_prev)**2 + (y - y_prev)**2 + (z - z_prev)**2)

    def sum_z_cal_relative_scale(self, R, t, q1, q2):

        #Trasformation matrix of first image
        T = self.transformation_matrix(R, t)
        #Projection matrix of second image
        P = np.matmul(np.concatenate((self.instrinsic_matrix, np.zeros((3, 1))), axis=1), T)

        hom_Q1 = cv2.triangulatePoints(self.projection_matrix, P, q1.T, q2.T)
        hom_Q2 = np.matmul(T, hom_Q1)

        # Un-homogenize
        uhom_Q1 = hom_Q1[:3, :] / hom_Q1[3, :]
        uhom_Q2 = hom_Q2[:3, :] / hom_Q2[3, :]

        # Check z coordinates
        sum_of_pos_z_Q1 = sum(uhom_Q1[2, :] > 0)
        sum_of_pos_z_Q2 = sum(uhom_Q2[2, :] > 0)

        # Form point pairs and calculate the relative scale
        Q1_matrix = uhom_Q1.T[:self.sample_scale]
        Q2_matrix = uhom_Q2.T[:self.sample_scale]

        Q1_matrix = np.linalg.norm(Q1_matrix[:-1] - Q1_matrix[1:], axis=-1)
        Q2_matrix = np.linalg.norm(Q2_matrix[:-1] - Q2_matrix[1:], axis=-1)

        Q1_matrix = np.delete(Q1_matrix, np.where(Q2_matrix==0))
        Q2_matrix = np.delete(Q2_matrix, np.where(Q2_matrix==0))
    
        if self.sample_scale: relative_scale = 1
        else:
            scale_matrix = Q1_matrix/Q2_matrix
            relative_scale = np.mean(scale_matrix)

        return sum_of_pos_z_Q1 + sum_of_pos_z_Q2, relative_scale

    @staticmethod
    def detecter_and_matcher(detect_method='SIFT', match_method = 'BF'):

        if match_method == 'BF':
            if detect_method == 'SIFT':
                return cv2.SIFT_create(nfeatures=3000), cv2.BFMatcher_create(cv2.NORM_L2, crossCheck=False)
            elif detect_method == 'ORB':
                return cv2.ORB_create(nfeatures=3000), cv2.BFMatcher_create(cv2.NORM_HAMMING2, crossCheck=False)

        elif match_method == 'FLANN':
            index_params_1 = dict(algorithm = 1, trees=5)
            index_params_6 = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=1)
            search_params = dict(checks=50)
            if detect_method == 'SIFT':
                return cv2.SIFT_create(nfeatures=3000), cv2.FlannBasedMatcher(index_params_1, search_params)
            elif detect_method == 'ORB':
                return cv2.ORB_create(nfeatures=3000), cv2.FlannBasedMatcher(index_params_6, search_params)

    def get_matches(self, i, display):

        next_kp, next_des = self.detecter.detectAndCompute(self.images[i], None)
        matches = self.matcher.knnMatch(self.des, next_des, k=2)
        matches = sorted(matches, key = lambda x:x[0].distance)

        good_list = []
        try:
            for m, n in matches:
                if m.distance < 0.7 * n.distance:
                    good_list.append(m)
        except:
            pass

        if display == True:
            img = cv2.drawMatches(self.images[i-1], self.kp, self.images[i], next_kp, good_list , 
                                None, matchColor=-1, singlePointColor=None, matchesMask=None, flags=2)
            cv2.imshow("image", img)
            cv2.waitKey(1)

        q1 = np.float32([self.kp[m.queryIdx].pt for m in good_list])
        q2 = np.float32([next_kp[m.trainIdx].pt for m in good_list])

        self.kp = next_kp
        self.des = next_des
        
        return q1, q2

    def decompose_essential_matrix(self, i, E, q1, q2):

        # Decompose the essential matrix
        R1, R2, t = cv2.decomposeEssentialMat(E)
        t = np.squeeze(t)

        z_sums = []
        relative_scales = []
        possible_solutions = [[R1, t], [R1, -t], [R2, t], [R2, -t]]
        
        for R, t in possible_solutions:
            z_sum, scale = self.sum_z_cal_relative_scale(R, t, q1, q2)
            z_sums.append(z_sum)
            relative_scales.append(scale)

        # Select the pair there has the most points with positive z coordinate
        right_pair_idx = np.argmax(z_sums)
        right_pair = possible_solutions[right_pair_idx]

        if self.sample_scale == 0: 
            relative_scale = 1
        elif self.sample_scale == 1:
            relative_scale = self.get_scale_gt(i)
        else:
            relative_scale = relative_scales[right_pair_idx]

        R, t = right_pair
        # print(relative_scale)
        t = t * relative_scale
        return R, t

    def get_pose(self, i, q1, q2):
   
        # Essential matrix
        # E, _ = cv2.findEssentialMat(q1, q2, self.instrinsic_matrix, threshold=1)
        E, _ = cv2.findEssentialMat(q1, q2, self.instrinsic_matrix, cv2.RANSAC, 0.999, 1.0, None)
        R, t = self.decompose_essential_matrix(i, E, q1, q2)

        return self.transformation_matrix(R, np.squeeze(t))






def visual_odometry(data_dir, detect_method, match_method, sample_scale, display, evaluate):

    model = Visual_Odometry(data_dir[1:], detect_method, match_method, sample_scale)
    plot = Plot(model.images)

    if display == True: plot.play_trip()

    ground_truth_path = []
    predict_path = []

    if evaluate == True: text_file = open("./results/evals/{}.txt".format(data_dir[0], detect_method, match_method), "w")

    for i, ground_truth_pose in enumerate(tqdm(model.ground_truth_poses, unit="pose", desc="Sequence {}".format(data_dir[0]))):

        if i == 0:
            current_pose = ground_truth_pose
        else:
            q1, q2 = model.get_matches(i, display)
            transformation_matrix = model.get_pose(i, q1, q2)

            current_pose = np.matmul(current_pose, np.linalg.inv(transformation_matrix))

        if evaluate == True:
            eval_array = current_pose[:3,:4].flatten()
            n = text_file.write(str(i) + ' ' + ' '.join(map(str,eval_array)) + '\n')

        ground_truth_path.append((ground_truth_pose[0, 3], ground_truth_pose[2, 3]))
        predict_path.append((current_pose[0, 3], current_pose[2, 3]))

    if display == True:
        cv2.destroyWindow("image")
        for i in range(5): cv2.waitKey(1) ### mac

    if evaluate == True: text_file.close()

    plot.save_paths(ground_truth_path, predict_path, data_dir[0], detect_method, match_method)
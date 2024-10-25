import os
import numpy as np
import cv2

class LoadKITTIdataset:

    def __init__(self, data_path, sequence):

        self.image_path = os.path.join(data_path, "sequences", sequence, "image_0")
        self.image_list = sorted(os.listdir(self.image_path))
        self.frame_idx = list(range(len(self.image_list)))

        calib_path = os.path.join(data_path, "sequences", sequence, "calib.txt")
        self.projection, self.intrinsic = self.load_calib(calib_path)
        
        pose_path = os.path.join(data_path, "poses", sequence+".txt")
        self.poses = self.load_poses(pose_path)

        self.sequence = int(sequence)

    def __iter__(self):
        self.idx = 0
        return self

    def __len__(self):
        return len(self.image_list)

    def __next__(self):
        if self.idx == len(self.frame_idx):
            raise StopIteration
        idx = self.frame_idx[self.idx]
        self.idx += 1

        image_path = os.path.join(self.image_path, self.image_list[idx])
        return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    @staticmethod
    def load_calib(file_path):
        """ Load projection matrix and intrinsic matrix. """
        with open(file_path, "r") as f:
            vec_string = np.fromstring(f.readline()[4:], dtype=np.float32, sep=" ") # P0
            mat_projection = vec_string.reshape(3, 4)
            mat_intrinsic = mat_projection[:3, :3]
        return mat_projection, mat_intrinsic

    @staticmethod
    def load_poses(file_path):
        """ Load ground truth SE(3) poses. """
        pose_list = []
        with open(file_path, "r") as f:
            for line in f.readlines():
                vec_line = np.fromstring(line, dtype=np.float32, sep=' ')
                pose = np.vstack((vec_line.reshape(3, 4), [0.0, 0.0, 0.0, 1.0]))
                pose_list.append(pose)
        return pose_list
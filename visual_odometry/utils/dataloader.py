import os
import numpy as np
import cv2
from tqdm import tqdm

class LoadKITTIdataset:

    def __init__(self, data_path, sequence):

        image_path = os.path.join(data_path, "sequences", sequence, "image_0")
        calib_path = os.path.join(data_path, "sequences", sequence, "calib.txt")
        pose_path = os.path.join(data_path, "poses", sequence+".txt")

        self.images = self.load_images(image_path)
        self.projection, self.intrinsic = self.load_calib(calib_path)
        self.poses = self.load_poses(pose_path)

    @staticmethod
    def load_images(file_path):
        """ Load monocular grayscale images. """
        image_list = []
        for file in tqdm(sorted(os.listdir(file_path)), unit="image", desc="Loading images"):
            image_path = os.path.join(file_path, file)
            image_list.append(cv2.imread(image_path, cv2.IMREAD_GRAYSCALE))
        return image_list

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
import os
import numpy as np
from tqdm import tqdm

class LoadKITTIdataset:

    def __init__(self, data_path, sequence):

        pcd_path = os.path.join(data_path, "sequences", sequence, "velodyne")
        calib_path = os.path.join(data_path, "sequences", sequence, "calib.txt")
        pose_path = os.path.join(data_path, "poses", sequence+".txt")

        self.pcd = self.load_pcd(pcd_path)
        self.lidar_to_camera = self.load_calib(calib_path)
        self.poses = self.load_poses(pose_path)

    

    @staticmethod
    def load_pcd(file_path):
        """ Load point clouds. """
        pcd_list = []
        pass

    @staticmethod
    def load_calib(file_path)

    


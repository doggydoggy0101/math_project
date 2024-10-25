import os
import numpy as np

class LoadKITTIdataset:

    def __init__(self, data_path, sequence):

        self.pcd_path = os.path.join(data_path, "sequences", sequence, "velodyne")
        self.pcd_list = sorted(os.listdir(self.pcd_path))
        self.frame_idx = list(range(len(self.pcd_list)))

        calib_path = os.path.join(data_path, "sequences", sequence, "calib.txt")
        self.lidar_to_camera = self.load_calib(calib_path)

        pose_path = os.path.join(data_path, "poses", sequence+".txt")
        self.poses = self.load_poses(pose_path)

        self.sequence = int(sequence)

    def __iter__(self):
        self.idx = 0
        return self

    def __len__(self):
        return len(self.pcd_list)

    def __next__(self):
        if self.idx == len(self.frame_idx):
            raise StopIteration
        idx = self.frame_idx[self.idx]
        self.idx += 1
    
        pcd_path = os.path.join(self.pcd_path, self.pcd_list[idx])
        pcd = np.fromfile(pcd_path, dtype=np.float32).reshape((-1, 4)) # (n, 4)
        #?QUESTION what is reflectance information (fourth dimension)
        return pcd 

    @staticmethod
    def load_calib(file_path):
        """ Load lidar to camera transformation matrix. """
        with open(file_path, "r") as f:
            vec_string = np.fromstring(f.readlines()[4][4:], dtype=np.float32, sep=" ") # Tr
        return np.vstack((vec_string.reshape(3, 4), [0.0, 0.0, 0.0, 1.0]))

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
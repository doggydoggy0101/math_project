import os
import numpy as np

class LoadKITTIdataset:

    def __init__(self, data_path, sequence):

        # Velodyne HDL-64E spec
        self.NUM_SCANS = 64
        self.SCAN_PERIOD = 0.1
        self.MIN_DISTANCE_THRES = 2.5
        self.MAX_DISTANCE_THRES = 120

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

        scan_ids = self._get_scan_ids(pcd) # 64 to 1
        rel_time = self._get_rel_time(pcd) # 0 to 1
        scan_info = scan_ids + self.SCAN_PERIOD * rel_time
        pcd = np.hstack((pcd, scan_info[:, np.newaxis])) # (n, 5), add scan_info

        pcd, scan_ids = self._remove_unreliable_points(pcd, scan_ids)

        # create index by the number of points for the 64 laser scan
        # scan_start = np.zeros(self.NUM_SCANS, dtype=int)
        # scan_end = np.zeros(self.NUM_SCANS, dtype=int)
        # _, elem_cnt = np.unique(scan_ids, return_counts=True)
        # start = 0
        # for ind, cnt in enumerate(elem_cnt):
        #     scan_start[ind] = start
        #     start += cnt
        #     scan_end[ind] = start
        # sorted_ind = np.argsort(scan_ids, kind='stable')
        # pcd = pcd[sorted_ind]

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


    def _get_scan_ids(self, pcd):
        # calculate pitch angle of each lidar point
        depth = np.linalg.norm(pcd, axis=1)
        pitch = np.arcsin(pcd[:, 2] / depth)
        # vertical fov: +2 up to -24.8 down with 64 equally angular subdivisions
        fov_down = -24.8 / 180 * np.pi
        fov = (abs(-24.8) + abs(2.0)) / 180 * np.pi
        scan_ids = (pitch + abs(fov_down)) / fov
        scan_ids *= self.NUM_SCANS
        scan_ids = np.floor(scan_ids).astype(np.int32)

        return scan_ids

    def _get_rel_time(self, pcd):
        start_ori = -np.arctan2(pcd[0, 1], pcd[0, 0])
        end_ori = -np.arctan2(pcd[-1, 1], pcd[-1, 0]) + 2 * np.pi
        if end_ori - start_ori > 3 * np.pi:
            end_ori -= 2 * np.pi
        elif end_ori - start_ori < np.pi:
            end_ori += 2 * np.pi

        half_passed = False
        num_points = pcd.shape[0]
        rel_time = np.zeros(num_points)

        for i in range(num_points):
            ori = -np.arctan2(pcd[i, 1], pcd[i, 0])
            if not half_passed:
                if ori < start_ori - np.pi / 2:
                    ori += 2 * np.pi
                elif ori > start_ori + np.pi * 3 / 2:
                    ori -= 2 * np.pi
                if ori - start_ori > np.pi:
                    half_passed = True
            else:
                ori += 2 * np.pi
                if ori < end_ori - np.pi * 3 / 2:
                    ori += 2 * np.pi
                elif ori > end_ori + np.pi / 2:
                    ori -= 2 * np.pi
            rel_time[i] = (ori - start_ori) / (end_ori - start_ori)
        return rel_time

    def _remove_unreliable_points(self, pcd, scan_ids):
        # remove points that are too close to the lidar
        dists = np.sum(pcd[:, :3] ** 2, axis=1)
        valid_mask1 = \
            (dists > self.MIN_DISTANCE_THRES ** 2) \
            & (dists < self.MAX_DISTANCE_THRES ** 2)

        # only keep points with scan id in a reasonable range [0, NUM_SCANS)
        valid_mask2 = np.logical_and(scan_ids >= 0, scan_ids < self.NUM_SCANS)

        valid_mask = np.logical_and(valid_mask1, valid_mask2)
        pcd = pcd[valid_mask]
        scan_ids = scan_ids[valid_mask]

        return pcd, scan_ids
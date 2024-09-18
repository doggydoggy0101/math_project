import numpy as np
from tqdm import tqdm

from model.registration import FGRandICP
from visualize.trajectory import plot_path

class LaserOdometryAndMapping:

    def __init__(self, voxel_size):

        self.registration = FGRandICP(voxel_size=voxel_size)

    def run(self, data, plot_trajectory=True):

        Tr = data.lidar_to_camera

        # log result
        log_file = open("./result/{0:0=2d}.txt".format(data.sequence), "w")
        # visualize path
        if plot_trajectory:
            pred_path = []
            gt_path = []

        for i, pcd in enumerate(tqdm(data, unit="point cloud", desc="LOAM")):

            gt_pose = data.poses[i]

            if i == 0:
                abs_pose = gt_pose
                pcd_previous = pcd 
             
            else:
                # registration
                T = self.registration.run(pcd_previous[:, :3], pcd[:, :3])
                
                # odometry 
                rel_pose = Tr@np.linalg.inv(T)@np.linalg.inv(Tr)
                abs_pose = abs_pose@rel_pose

                #TODO lidar mapping

                if plot_trajectory: # (x, z)
                    pred_path.append((abs_pose[0, 3], abs_pose[2, 3])) 
                    gt_path.append((gt_pose[0, 3], gt_pose[2, 3]))
                
                pcd_previous = pcd 

            # log poses (format) i T00 T01 T02 T03 T10 T11 T12 T13 T20 T21 T22 T23 
            vec_pose = abs_pose[:3, :4].flatten()
            n = log_file.write(str(i) + ' ' + ' '.join(map(str, vec_pose)) + '\n')

        log_file.close()

        if plot_trajectory:
            plot_path(pred_path, gt_path, data.sequence)


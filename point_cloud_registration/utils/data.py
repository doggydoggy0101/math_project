import numpy as np
import copy
import open3d as o3d
from utils.error import projectionError

class createBunnyDataset:
    def __init__(self, num, translation, rotation, 
                 noise_std=0.01, outlier_rate=0.5, outlier_scale=5, verbose=False, random_state=42):
        
        self.num_point = num
        self.rng = random_state

        self.translation = translation
        self.rotation = rotation

        ### make bunny dataset
        dataset = o3d.data.BunnyMesh()
        mesh = o3d.io.read_triangle_mesh(dataset.path)
        o3d.utility.random.seed(self.rng) # fix random seed
        self.pcd1 = mesh.sample_points_poisson_disk(number_of_points=self.num_point)
        self.pcd1.scale(1/np.max(self.pcd1.get_max_bound()-self.pcd1.get_min_bound()), center=self.pcd1.get_center()) # normalize
        self.pcd1.translate(-self.pcd1.get_center()) # align center to (0,0,0)


        ### apply noise 
        self.pcd2 = self.apply_noise(self.pcd1, mu=0, sigma=noise_std)
        ### apply spatial transformation
        self.pcd2.rotate(self.rotation)
        self.pcd2.translate(self.translation)
        ### apply outliers
        self.pcd2 = self.apply_outliers(self.pcd2, rate=outlier_rate, scale=outlier_scale)


        self.pcd1point = np.asarray(self.pcd1.points)
        self.pcd2point = np.asarray(self.pcd2.points)

        self.pcd1inlier = self.pcd1point[self.inliers, :]
        self.pcd2inlier = self.pcd2point[self.inliers, :]

        self.pcd1.paint_uniform_color(np.array([41, 128, 185])/255) # blue
        self.pcd2.paint_uniform_color(np.array([231, 76, 60])/255) # red

        self.projection_error = projectionError(self.pcd1point, self.pcd2point, self.rotation, self.translation).projection_error
        
        if verbose:
            print("-"*10 + " Bunny dataset " + "-"*10)
            print("rng:", self.rng)
            print("points", self.num_point)
            print("ground truth rotation:\n", self.rotation)
            print("ground truth translation:", self.translation)
            print("projection error:", np.round(self.projection_error, 3))
            
    def apply_noise(self, pcd, mu, sigma):

        noisy_pcd = copy.deepcopy(pcd)
        points = np.asarray(noisy_pcd.points)

        np.random.seed(self.rng) # fix random seed
        points += np.random.normal(mu, sigma, size=points.shape)

        noisy_pcd.points = o3d.utility.Vector3dVector(points)
        return noisy_pcd

    def apply_outliers(self, pcd, rate, scale):

        points = np.asarray(pcd.points)

        np.random.seed(self.rng) # fix random seed
        self.outliers = np.sort(np.random.choice(self.num_point, int(self.num_point*rate), replace=False))

        self.inliers = []
        for inlier in range(self.num_point):
            if inlier not in self.outliers:
                self.inliers.append(inlier)

        center = pcd.get_center()
        np.random.seed(self.rng) # fix random seed
        for i in self.outliers: 
            points[i] = center + (np.random.rand(3) - 1/2)*scale

        pcd.points = o3d.utility.Vector3dVector(points)
        return pcd
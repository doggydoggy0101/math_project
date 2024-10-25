import open3d as o3d

class FGRandICP:

    def __init__(self, voxel_size=1):

        self.voxel_size = voxel_size

    def preprocess_point_cloud(self, pcd):
        """ FPFH feature extraction. """
        pcd_down = pcd.voxel_down_sample(self.voxel_size)
        radius_normal = self.voxel_size*2
        pcd_down.estimate_normals(
            o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

        radius_feature = self.voxel_size*5
        pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
            pcd_down,
            o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
        return pcd_down, pcd_fpfh

    def fast_global_registration(self, source_down, target_down, source_fpfh, target_fpfh):
        distance_threshold = self.voxel_size*0.5
        result = o3d.pipelines.registration.registration_fgr_based_on_feature_matching(
            source_down, target_down, source_fpfh, target_fpfh,
            o3d.pipelines.registration.FastGlobalRegistrationOption(
                maximum_correspondence_distance=distance_threshold))
        return result

    def refine_registration(self, source, target, initial):
        distance_threshold = self.voxel_size*0.4
        result = o3d.pipelines.registration.registration_icp(
            source, target, distance_threshold, initial,
            o3d.pipelines.registration.TransformationEstimationPointToPlane())
        return result

    def run(self, pcd1, pcd2):

        source = o3d.geometry.PointCloud()
        source.points = o3d.utility.Vector3dVector(pcd1)
        source.estimate_normals()
        
        target = o3d.geometry.PointCloud()
        target.points = o3d.utility.Vector3dVector(pcd2)
        target.estimate_normals()

        # down sample 
        source_down = source.voxel_down_sample(self.voxel_size)
        target_down = target.voxel_down_sample(self.voxel_size)
        self.voxel_size = 2

        # doubledown sample & feature extraction
        source_ddown, source_fpfh = self.preprocess_point_cloud(source)
        target_ddown, target_fpfh = self.preprocess_point_cloud(target)

        # global registration by FGR
        result_fgr = self.fast_global_registration(source_ddown, target_ddown, source_fpfh, target_fpfh)
        # local refinement by ICP
        result_icp = self.refine_registration(source_down, target_down, initial=result_fgr.transformation)

        return result_icp.transformation
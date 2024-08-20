import numpy as np

class computeError:
    def __init__(self, estimated_rotation=None, estimated_translation=None,
                       gtruth_rotation=None, gtruth_translation=None, verbose=False):

        if estimated_rotation is not None:
            self.rotation_error = self.rotationError(estimated_rotation, gtruth_rotation)
            if verbose:
                print("rotation error:", np.round(self.rotation_error, 5), "(degree)")
                
        if estimated_translation is not None:
            self.translation_error = self.translationError(estimated_translation, gtruth_translation)
            if verbose:
                print("translation error:", np.round(self.translation_error, 5), "(norm)")

    def rotationError(self, rotation, gtruth):
        
        val = (np.trace(rotation.T@gtruth) - 1)/2
        if val > 1: 
            val = 1
        if val < -1: 
            val = -1  
            
        return np.arccos(val)

    def translationError(self, translation, gtruth):
        return np.linalg.norm(translation - gtruth)



class projectionError:
    def __init__(self, pcd1, pcd2, rotation=None, translation=None, verbose=False):

        if rotation is None:
            rotation = np.eye(3)
        if translation is None:
            translation = np.zeros(3)

        self.estimated_pcd = (rotation@pcd1.T).T + translation
        self.projection_error = self.residual(self.estimated_pcd, pcd2)

        if verbose:
            print("projection error:", np.round(self.projection_error, 3))

    def residual(self, estimate, gtruth):

        res = np.linalg.norm(gtruth - estimate, axis=1, ord=2)

        return np.sum(res**2)
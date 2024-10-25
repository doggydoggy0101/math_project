import cv2

class FeatureDetectingAndMatching:
    """ Return CV2 feature detecter and matcher. """

    def __init__(self, detect_method="ORB", match_method="FLANN"):

        self.detecter, self.mathcher = self.detecter_and_matcher(detect_method, match_method)

    @staticmethod
    def detecter_and_matcher(detect_method, match_method):

        if match_method == 'BF':
            if detect_method == 'SIFT':
                detecter = cv2.SIFT_create(nfeatures=3000)
                matcher = cv2.BFMatcher_create(cv2.NORM_L2, crossCheck=False)
            elif detect_method == 'ORB':
                detecter =  cv2.ORB_create(nfeatures=3000)
                matcher = cv2.BFMatcher_create(cv2.NORM_HAMMING2, crossCheck=False)

        elif match_method == 'FLANN':
            index_params_1 = dict(algorithm=1, trees=5)
            index_params_6 = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=1)
            search_params = dict(checks=50)
            if detect_method == 'SIFT':
                detecter = cv2.SIFT_create(nfeatures=3000)
                matcher = cv2.FlannBasedMatcher(index_params_1, search_params)
            elif detect_method == 'ORB':
                detecter = cv2.ORB_create(nfeatures=3000)
                matcher = cv2.FlannBasedMatcher(index_params_6, search_params)
        else:
            print("Detect method or Match method not supported by CV2.")
            print("-> shoud be one of SIFT/BF, SIFT/FLANN, ORB/BF, ORB/FLANN")
            print("-> exit")
            exit(1)

        return detecter, matcher
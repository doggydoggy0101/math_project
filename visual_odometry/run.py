from visual_odometry import visual_odometry
from evaluation import evaluate

def make_dir(data):
    """ data structure should be as follows (KITTI dataset) """

    image_dir = './dataset/sequences/' + data + '/image_0' 
    calib_dir = './dataset/sequences/' + data + '/calib.txt'
    poses_dir = './dataset/poses/' + data + '.txt'

    return [data, image_dir, calib_dir, poses_dir]

def main(display=False, eval_=True):

    data = "test2"
    detect_method = "ORB" # ORB, SIFT
    match_method = "FLANN" # BF, FLANN
    sample_scale = 1 # 0 is none, 1 is from ground truth
    align = "6dof" # 'scale', 'scale_7dof', '7dof', '6dof'

    visual_odometry(make_dir(data), detect_method, match_method, sample_scale, display, eval_)
    evaluate("results/evals".format(data), align, [data])

main()
from utils.dataloader import LoadKITTIdataset
from model.vo import VisualOdometry
from visualize.trajectory import plot_path

SEQUENCE="09"

data = LoadKITTIdataset(data_path="data", sequence=SEQUENCE)
model = VisualOdometry(detect_method="ORB", match_method="FLANN")
model.run(data)

plot_path(model.pred_path, model.gt_path, SEQUENCE)
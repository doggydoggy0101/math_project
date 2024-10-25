from utils.dataloader import LoadKITTIdataset
from model.vo import VisualOdometry
from utils.evaluate import EvalOdometry

SEQUENCE="10"

data = LoadKITTIdataset(data_path="data", sequence=SEQUENCE)
model = VisualOdometry(detect_method="ORB", match_method="FLANN")
model.run(data)

EvalOdometry().run(sequence=SEQUENCE, alignment="6dof")
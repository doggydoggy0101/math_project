from utils.dataloader import LoadKITTIdataset
from model.loam import LaserOdometryAndMapping
from utils.evaluate import EvalOdometry

SEQUENCE="10"

data = LoadKITTIdataset(data_path="data", sequence=SEQUENCE)
model = LaserOdometryAndMapping(voxel_size=1)
model.run(data)

EvalOdometry().run(sequence=SEQUENCE, alignment="6dof")
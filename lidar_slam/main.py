from utils.dataloader import LoadKITTIdataset
from model.loam import LaserOdometryAndMapping
from utils.evaluate import EvalOdometry

SEQUENCE="09"

data = LoadKITTIdataset(data_path="data", sequence=SEQUENCE)
model = LaserOdometryAndMapping()
model.run(data)

EvalOdometry().run(sequence=SEQUENCE, alignment="6dof")
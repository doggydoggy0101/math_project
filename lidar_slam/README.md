# :minidisc: Lidar Odometry and Mapping (LOAM)


### :file_folder: Dataset
Put the KITTI dataset in `data` as follows:
```
data
|--- poses
    |--- 00.txt
    |--- 01.txt
    |--- ...
|--- sequences
    |--- 00
        |--- velodyne
        |--- calib.txt
    |--- 01
    |--- ...
```

### :dog: Usage
```shell
python ./main.py
```
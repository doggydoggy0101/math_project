clc;clear;

baseDownloadURL = "https://cvg.cit.tum.de/rgbd/dataset/freiburg3/rgbd_dataset_freiburg3_long_office_household.tgz"; 
dataFolder      = 'dataset'; 
options         = weboptions(Timeout=Inf);
tgzFileName     = [dataFolder, 'fr3_office.tgz'];
folderExists    = exist(dataFolder, "dir");

if ~folderExists  
    mkdir(dataFolder); 
    disp('Downloading fr3_office.tgz (1.38 GB)...') 
    websave(tgzFileName, baseDownloadURL, options); 
    disp('Extracting fr3_office.tgz (1.38 GB) ...') 
    untar(tgzFileName, dataFolder); 
end

imageFolder = fullfile(dataFolder,'rgbd_dataset_freiburg3_long_office_household/rgb/');
imds = imageDatastore(imageFolder);

% check
currFrameIdx = 11;
currI = readimage(imds, currFrameIdx);
himage = imshow(currI);
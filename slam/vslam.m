clc;clear;rng(0);
addpath(genpath('main')); addpath(genpath('utils')); addpath(genpath('visualize')); 

imageFolder = 'dataset/rgbd_dataset_freiburg3_long_office_household/rgb/';

imds = imageDatastore(imageFolder);
numFrames = numel(imds.Files);

% KITTI 07
% focalLength = [707.0912, 707.0912];
% principalPoint = [601.8873, 183.1104];

% TUM
focalLength = [535.4, 539.2]; 
principalPoint = [320.1, 247.6];  



% paramters
scaleFactor = 1.2; numLevels = 8; % image pyramid
numPoints = 1000; % uniform distributed feature points
matchUnique = true; maxRatio = 0.9; matchThreshold = 20;
minMatches = 40; % match point threshold
ratioThreshold = 0.45; % homography/fundamental
minParallax = 1; % degree
absTor = 1e-7; relTor = 1e-15; % BA
baSolver = "preconditioned-conjugate-gradient";



% check
currFrameIdx = 1;
currI = readimage(imds, currFrameIdx);

imageSize = size(currI,[1 2]); 
% store intrinsic parameters (Matlab function) 
intrinsics = cameraIntrinsics(focalLength, principalPoint, imageSize);
% feature extraction
[preFeatures, prePoints] = feature_detection(currI, scaleFactor, numLevels, numPoints); 

currFrameIdx = currFrameIdx + 1;
firstI = currI;



% map initialization
[relPose, xyzWorldPoints, indexPairs, currPoints, currFeatures] = map_initialization(intrinsics, imds, currFrameIdx, numFrames, preFeatures, prePoints, ...
    scaleFactor, numLevels, numPoints, matchUnique, maxRatio, matchThreshold, minMatches, ratioThreshold, minParallax);



% graph initialization
preViewId = 1; currViewId = 2;

vSetKeyFrames = imageviewset; % store key frames
mapPointSet = worldpointset; % store map points

[vSetKeyFrames, mapPointSet, newPointIdx, preLocations, currLocations, preScales, currScales] = graph_initialization(vSetKeyFrames, mapPointSet, ...
    indexPairs, relPose, xyzWorldPoints, preViewId, currViewId, prePoints, currPoints, preFeatures, currFeatures);



% bow initialization (for loop detection)
[loopDatabase] = bow_initialization(preViewId, currViewId, preFeatures, currFeatures);



% bundle adjustment (Matlab function)
tracks = findTracks(vSetKeyFrames);
cameraPoses = poses(vSetKeyFrames);

[refinedPoints, refinedAbsPoses] = bundleAdjustment(xyzWorldPoints, tracks, cameraPoses, intrinsics, FixedViewIDs=1, ...
    PointsUndistorted=true, AbsoluteTolerance=absTor, RelativeTolerance=relTor, MaxIteration=20, Solver=baSolver);


% scaling with median depth of 3d points
[relPose, refinedPoints, refinedAbsPoses] = scaling(relPose, currViewId, refinedPoints, refinedAbsPoses);



% update graph
[vSetKeyFrames, mapPointSet] = graph_update(vSetKeyFrames, mapPointSet, newPointIdx, relPose, preViewId, currViewId, refinedAbsPoses, refinedPoints);



% visualization
featurePlot = visualize_matched_features(currI, currPoints(indexPairs(:,2)));
mapPlot = visualize_MfS(vSetKeyFrames, mapPointSet);
showLegend(mapPlot);



currKeyFrameId = currViewId;
lastKeyFrameId = currViewId;
lastKeyFrameIdx  = currFrameIdx - 1; 
addedFramesIdx = [1; lastKeyFrameIdx];
isLoopClosed = false;



% Main loop
isLastFrameKeyFrame = true;
while ~isLoopClosed && currFrameIdx < numFrames
    currI = readimage(imds, currFrameIdx);

    [currFeatures, currPoints] = feature_detection(currI, scaleFactor, numLevels, numPoints);

    % mapPointsIdx -> Indices of the map points observed in the current frame
    % featureIdx -> Indices of the corresponding feature points in the current frame
    [currPose, mapPointsIdx, featureIdx] = track_last_keyframe(mapPointSet, vSetKeyFrames.Views, ...
        currFeatures, currPoints, lastKeyFrameId, intrinsics, scaleFactor);

    % localKeyFrameIds -> ViewId of the connected key frames of the current frame
    numSkipFrames = 20; % keyframe gap
    numPointsKeyFrame = 100; % map points
    [localKeyFrameIds, currPose, mapPointsIdx, featureIdx, isKeyFrame] = track_local_map(mapPointSet, vSetKeyFrames, ...
        mapPointsIdx, featureIdx, currPose, currFeatures, currPoints, intrinsics, scaleFactor, numLevels, ...
        isLastFrameKeyFrame, lastKeyFrameIdx, currFrameIdx, numSkipFrames, numPointsKeyFrame);

    % Visualize matched features
    updatePlot(featurePlot, currI, currPoints(featureIdx));

    if ~isKeyFrame
        currFrameIdx = currFrameIdx + 1;
        isLastFrameKeyFrame = false;
        continue
    else
        isLastFrameKeyFrame = true;
    end

    currKeyFrameId = currKeyFrameId + 1;

    [mapPointSet, vSetKeyFrames] = add_keyframe(mapPointSet, vSetKeyFrames, ...
        currPose, currFeatures, currPoints, mapPointsIdx, featureIdx, localKeyFrameIds);

    % remove outlier
    outlierIdx = setdiff(newPointIdx, mapPointsIdx);
    if ~isempty(outlierIdx)
        mapPointSet = removeWorldPoints(mapPointSet, outlierIdx);
    end

    % triangulation
    minNumMatches = 10;
    minParallax = 3;
    [mapPointSet, vSetKeyFrames, newPointIdx] = create_map_points(mapPointSet, vSetKeyFrames, ...
        currKeyFrameId, intrinsics, scaleFactor, minNumMatches, minParallax);

    % local bundle adjustment
    [refinedViews, dist] = connectedViews(vSetKeyFrames, currKeyFrameId, MaxDistance=2);
    refinedKeyFrameIds = refinedViews.ViewId;
    fixedViewIds = refinedKeyFrameIds(dist==2);
    fixedViewIds = fixedViewIds(1:min(10, numel(fixedViewIds)));

    % bundle adjustment
    [mapPointSet, vSetKeyFrames, mapPointIdx] = bundleAdjustment(mapPointSet, vSetKeyFrames, ...
        [refinedKeyFrameIds; currKeyFrameId], intrinsics, FixedViewIDs=fixedViewIds, PointsUndistorted=true, ...
        AbsoluteTolerance=absTor, RelativeTolerance=relTor, Solver=baSolver, MaxIteration=10);

    mapPointSet = updateLimitsAndDirection(mapPointSet, mapPointIdx, vSetKeyFrames.Views);
    mapPointSet = updateRepresentativeView(mapPointSet, mapPointIdx, vSetKeyFrames.Views);
    updatePlot(mapPlot, vSetKeyFrames, mapPointSet);

    % Check loop closure after some key frames have been created    
    if currKeyFrameId > 20

        loopEdgeNumMatches = 50; % num of feature matches of loop edges

        [isDetected, validLoopCandidates] = loop_closure(vSetKeyFrames, currKeyFrameId, ...
            loopDatabase, currI, loopEdgeNumMatches);

        if isDetected 
            [isLoopClosed, mapPointSet, vSetKeyFrames] = loop_connections(...
                mapPointSet, vSetKeyFrames, validLoopCandidates, currKeyFrameId, ...
                currFeatures, loopEdgeNumMatches);
        end
    end

    if ~isLoopClosed
        addImageFeatures(loopDatabase,  currFeatures, currKeyFrameId);
    end

    lastKeyFrameId = currKeyFrameId;
    lastKeyFrameIdx = currFrameIdx;
    addedFramesIdx = [addedFramesIdx; currFrameIdx]; %#ok<AGROW>
    currFrameIdx = currFrameIdx + 1;
    
end 


if isLoopClosed
    minNumMatches = 20;
    vSetKeyFramesOptim = optimizePoses(vSetKeyFrames, minNumMatches, Tolerance=1e-16);

    mapPointSet = pose_graph(mapPointSet, vSetKeyFrames, vSetKeyFramesOptim);
    updatePlot(mapPlot, vSetKeyFrames, mapPointSet);
    optimizedPoses  = poses(vSetKeyFramesOptim);

    plotOptimizedTrajectory(mapPlot, optimizedPoses)
    showLegend(mapPlot);
end

% Load ground truth 
gTruthData = load("orbslamGroundTruth.mat");
gTruth = gTruthData.gTruth;

% Plot the actual camera trajectory 
plotActualTrajectory(mapPlot, gTruth(addedFramesIdx), optimizedPoses);

% Show legend
showLegend(mapPlot);

trajectory_error(gTruth(addedFramesIdx), optimizedPoses);

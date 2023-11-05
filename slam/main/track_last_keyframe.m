%   Copyright 2019-2022 The MathWorks, Inc.
function [currPose, mapPointIdx, featureIdx] = track_last_keyframe(...
    mapPoints, views, currFeatures, currPoints, lastKeyFrameId, intrinsics, scaleFactor)

% Get features from the last key frame that are in the map points
[index3d, index2d]    = findWorldPointsInView(mapPoints, lastKeyFrameId);
lastKeyFrameFeatures  = views.Features{lastKeyFrameId}(index2d,:);
lastKeyFramePoints    = views.Points{lastKeyFrameId}(index2d);

% Match features from the last key frame with the current key frame
indexPairs  = matchFeatures(currFeatures, binaryFeatures(lastKeyFrameFeatures), Unique=true, MaxRatio=0.9, MatchThreshold=40);

% Estimate the camera pose
matchedImagePoints = currPoints.Location(indexPairs(:,1),:);
matchedWorldPoints = mapPoints.WorldPoints(index3d(indexPairs(:,2)), :);
matchedImagePoints = cast(matchedImagePoints, like=matchedWorldPoints); % cast to same data type
[currPose, inlier, status] = estworldpose(matchedImagePoints, matchedWorldPoints, intrinsics, Confidence=95, MaxReprojectionError=3, MaxNumTrials=1e4);

% threshold
if status
    currPose=[];
    mapPointIdx=[];
    featureIdx=[];
    return
end

% Refine camera pose only
currPose = bundleAdjustmentMotion(matchedWorldPoints(inlier,:), matchedImagePoints(inlier,:), currPose, intrinsics, ...
    PointsUndistorted=true, AbsoluteTolerance=1e-7, RelativeTolerance=1e-15, MaxIteration=20);

% Search for more matches with the map points in the previous key frame
xyzPoints = mapPoints.WorldPoints(index3d,:);

[projectedPoints, isInImage] = world2img(xyzPoints, pose2extr(currPose), intrinsics);
projectedPoints = projectedPoints(isInImage, :);

minScales = max(1, lastKeyFramePoints.Scale(isInImage)/scaleFactor);
maxScales = lastKeyFramePoints.Scale(isInImage)*scaleFactor;
r = 4;
searchRadius = r*lastKeyFramePoints.Scale(isInImage);

indexPairs = matchFeaturesInRadius(binaryFeatures(lastKeyFrameFeatures(isInImage,:)), ...
    binaryFeatures(currFeatures.Features), currPoints, projectedPoints, searchRadius, ...
    MatchThreshold=40, MaxRatio=0.8, Unique=true);

if size(indexPairs, 1) < 20
    indexPairs = matchFeaturesInRadius(binaryFeatures(lastKeyFrameFeatures(isInImage,:)), ...
        binaryFeatures(currFeatures.Features), currPoints, projectedPoints, 2*searchRadius, ...
        MatchThreshold=40, MaxRatio=1, Unique=true);
end

% threshold
if size(indexPairs, 1) < 1
    currPose=[];
    mapPointIdx=[];
    featureIdx=[];
    return
end

% Filter by scales
isGoodScale = currPoints.Scale(indexPairs(:, 2)) >= minScales(indexPairs(:, 1)) & ...
    currPoints.Scale(indexPairs(:, 2)) <= maxScales(indexPairs(:, 1));
indexPairs = indexPairs(isGoodScale, :);

% Obtain the index of matched map points and features
tempIdx = find(isInImage); % Convert to linear index
mapPointIdx = index3d(tempIdx(indexPairs(:,1)));
featureIdx = indexPairs(:,2);

% Refine the camera pose again
matchedWorldPoints = mapPoints.WorldPoints(mapPointIdx, :);
matchedImagePoints = currPoints.Location(featureIdx, :);

currPose = bundleAdjustmentMotion(matchedWorldPoints, matchedImagePoints, currPose, intrinsics, ...
    PointsUndistorted=true, AbsoluteTolerance=1e-7, RelativeTolerance=1e-15, MaxIteration=20);

end
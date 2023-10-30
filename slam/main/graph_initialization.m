function [vSetKeyFrames, mapPointSet, newPointIdx, preLocations, currLocations, preScales, currScales] = graph_initialization(vSetKeyFrames, mapPointSet, ...
    indexPairs, relPose, xyzWorldPoints, preViewId, currViewId, prePoints, currPoints, preFeatures, currFeatures)

    % set first keyframe at the origin
    vSetKeyFrames = addView(vSetKeyFrames, preViewId, rigidtform3d, Points=prePoints, Features=preFeatures.Features);
    % set second keyframe by relative pose (equivalent to absolute pose)
    vSetKeyFrames = addView(vSetKeyFrames, currViewId, relPose, Points=currPoints, Features=currFeatures.Features);
    % add relative pose between first and second keyframe
    vSetKeyFrames = addConnection(vSetKeyFrames, preViewId, currViewId, relPose, Matches=indexPairs);
    % add 3d points
    [mapPointSet, newPointIdx] = addWorldPoints(mapPointSet, xyzWorldPoints);
    % add correspondence between first key frame and 3d points
    mapPointSet = addCorrespondences(mapPointSet, preViewId, newPointIdx, indexPairs(:,1));
    % add correspondence between second key frame and 3d points
    mapPointSet = addCorrespondences(mapPointSet, currViewId, newPointIdx, indexPairs(:,2));
    
    % observations of 3d points
    preLocations = prePoints.Location; % pixel coordinate
    currLocations = currPoints.Location; % pixel coordinate
    preScales = prePoints.Scale; % decomposition scale
    currScales = currPoints.Scale; % decomposition scale

end


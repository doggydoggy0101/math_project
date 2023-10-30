function [isLoopClosed, mapPoints, vSetKeyFrames] = loop_connections(...
    mapPoints, vSetKeyFrames, loopCandidates, currKeyFrameId, currFeatures, ...
    loopEdgeNumMatches)
%helperAddLoopConnections add connections between the current key frame and
%   the valid loop candidate key frames. A loop candidate is valid if it has
%   enough covisible map points with the current key frame.

%   This is an example helper function that is subject to change or removal
%   in future releases.

%   Copyright 2019-2022 The MathWorks, Inc.

loopClosureEdge = [];

numCandidates   = size(loopCandidates,1);
[index3d1, index2d1] = findWorldPointsInView(mapPoints, currKeyFrameId);
validFeatures1  = currFeatures.Features(index2d1, :);

for k = 1 : numCandidates
    [index3d2, index2d2] = findWorldPointsInView(mapPoints, loopCandidates(k));
    allFeatures2   = vSetKeyFrames.Views.Features{loopCandidates(k)};
    validFeatures2 = allFeatures2(index2d2, :);
    
    indexPairs = matchFeatures(binaryFeatures(validFeatures1), binaryFeatures(validFeatures2), ...
        'Unique', true, 'MaxRatio', 0.9, 'MatchThreshold', 40);
    
    % Check if all the candidate key frames have strong connection with the
    % current keyframe
    if size(indexPairs, 1) < loopEdgeNumMatches
        continue
    end
    
    % Estimate the relative pose of the current key frame with respect to the
    % loop candidate keyframe with the highest similarity score
    
    worldPoints1 = mapPoints.WorldPoints(index3d1(indexPairs(:, 1)), :);
    worldPoints2 = mapPoints.WorldPoints(index3d2(indexPairs(:, 2)), :);
    
    tform1 = pose2extr(vSetKeyFrames.Views.AbsolutePose(end));
    tform2 = pose2extr(vSetKeyFrames.Views.AbsolutePose(loopCandidates(k)));
    
    worldPoints1InCamera1 = transformPointsForward(tform1, worldPoints1) ;
    worldPoints2InCamera2 = transformPointsForward(tform2, worldPoints2) ;

    w = warning('off','all');
    [tform, inlierIndex] = estgeotform3d(...
        worldPoints1InCamera1, worldPoints2InCamera2, 'similarity', 'MaxDistance', 0.1);
    warning(w);

    % Add connection between the current key frame and the loop key frame
    matches = uint32([index2d2(indexPairs(inlierIndex, 2)), index2d1(indexPairs(inlierIndex, 1))]);
    vSetKeyFrames = addConnection(vSetKeyFrames, loopCandidates(k), currKeyFrameId, tform, 'Matches', matches);
    
    % Fuse co-visible map points
    matchedIndex3d1 = index3d1(indexPairs(inlierIndex, 1));
    matchedIndex3d2 = index3d2(indexPairs(inlierIndex, 2));
    mapPoints = updateWorldPoints(mapPoints, matchedIndex3d1, mapPoints.WorldPoints(matchedIndex3d2, :));
    
    loopClosureEdge = [loopClosureEdge; loopCandidates(k), currKeyFrameId];
end
isLoopClosed = ~isempty(loopClosureEdge);
end
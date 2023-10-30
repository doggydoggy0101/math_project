function [vSetKeyFrames, mapPointSet] = graph_update(vSetKeyFrames, mapPointSet, newPointIdx, relPose, preViewId, currViewId, refinedAbsPoses, refinedPoints)

    % Update key frames with the refined poses
    vSetKeyFrames = updateView(vSetKeyFrames, refinedAbsPoses);
    vSetKeyFrames = updateConnection(vSetKeyFrames, preViewId, currViewId, relPose);
    
    % Update map points with the refined positions
    mapPointSet = updateWorldPoints(mapPointSet, newPointIdx, refinedPoints);
    
    % Update view direction and depth 
    mapPointSet = updateLimitsAndDirection(mapPointSet, newPointIdx, vSetKeyFrames.Views);
    
    % Update representative view
    mapPointSet = updateRepresentativeView(mapPointSet, newPointIdx, vSetKeyFrames.Views);

end


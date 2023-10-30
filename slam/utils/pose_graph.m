function mapPointSet = pose_graph(mapPointSet, vSetKeyFrames, vSetKeyFramesOptim)
    
    % update map points after PGO
    posesOld = vSetKeyFrames.Views.AbsolutePose;
    posesNew = vSetKeyFramesOptim.Views.AbsolutePose;
    
    positionsOld = mapPointSet.WorldPoints;
    positionsNew = positionsOld;
    
    indices = 1:mapPointSet.Count;
    
    % Update world location of map point based on the new absolute pose of the corresponding major view
    for i = indices
        majorViewIds = mapPointSet.RepresentativeViewId(i);
        poseNew = posesNew(majorViewIds).A;
        tform = affinetform3d(poseNew/posesOld(majorViewIds).A);
        positionsNew(i, :) = transformPointsForward(tform, positionsOld(i, :));
    end
    
    mapPointSet = updateWorldPoints(mapPointSet, indices, positionsNew);

end
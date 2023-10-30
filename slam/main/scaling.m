function [relPose, refinedPoints, refinedAbsPoses] = scaling(relPose, currViewId, refinedPoints, refinedAbsPoses)

    medianDepth = median(vecnorm(refinedPoints.'));
    refinedPoints = refinedPoints / medianDepth;
    refinedAbsPoses.AbsolutePose(currViewId).Translation = refinedAbsPoses.AbsolutePose(currViewId).Translation / medianDepth;
    relPose.Translation = relPose.Translation / medianDepth;

end


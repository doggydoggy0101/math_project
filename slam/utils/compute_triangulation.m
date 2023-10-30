function [isValid, xyzPoints, inlierIdx] = compute_triangulation(pose1, pose2, matchedPoints1, matchedPoints2, intrinsics, minParallax)

    camMatrix1 = cameraProjection(intrinsics, pose2extr(pose1));
    camMatrix2 = cameraProjection(intrinsics, pose2extr(pose2));
    
    [xyzPoints, reprojectionErrors, isInFront] = triangulate(matchedPoints1, matchedPoints2, camMatrix1, camMatrix2);
    
    % Filter points by view direction and reprojection error
    minReprojError = 1;
    inlierIdx = isInFront & reprojectionErrors < minReprojError;
    xyzPoints = xyzPoints(inlierIdx,:);
    
    % A good two-view with significant parallax
    ray1 = xyzPoints - pose1.Translation;
    ray2 = xyzPoints - pose2.Translation;
    cosAngle = sum(ray1 .* ray2, 2) ./ (vecnorm(ray1, 2, 2) .* vecnorm(ray2, 2, 2));
    
    % Check parallax
    isValid = all(cosAngle < cosd(minParallax) & cosAngle>0);
    
end
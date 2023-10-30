function [features, validPoints] = feature_detection(Irgb, scaleFactor, numLevels, numPoints, varargin)

    Igray  = im2gray(Irgb);
    % ORB feature detection
    points = detectORBFeatures(Igray, ScaleFactor=scaleFactor, NumLevels=numLevels);
    % keypoint selection
    points = selectUniform(points, numPoints, size(Igray, 1:2));
    % extract features
    [features, validPoints] = extractFeatures(Igray, points, Method="ORB");

end
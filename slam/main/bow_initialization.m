function [loopDatabase] = bow_initialization(preViewId, currViewId, preFeatures, currFeatures)
addpath(genpath('./bow'));

    bofData = load("bagOfFeaturesDataSLAM.mat");

    % Initialize the place recognition database
    loopDatabase = invertedImageIndex(bofData.bof, SaveFeatureLocations=false);

    % Add features of the first two key frames to the database
    addImageFeatures(loopDatabase, preFeatures, preViewId);
    addImageFeatures(loopDatabase, currFeatures, currViewId);

end


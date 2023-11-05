function [relPose, xyzWorldPoints, indexPairs, currPoints, currFeatures, currFrameIdx] = map_initialization(intrinsics, imds, currFrameIdx, numFrames, preFeatures, prePoints, ...
    scaleFactor, numLevels, numPoints, matchUnique, maxRatio, matchThreshold, minMatches, ratioThreshold, minParallax)
addpath(genpath('./utils'))

    isMapInitialized  = false;
    while ~isMapInitialized && currFrameIdx < numFrames
    
        currI = readimage(imds, currFrameIdx);
        [currFeatures, currPoints] = feature_detection(currI, scaleFactor, numLevels, numPoints); 
        currFrameIdx = currFrameIdx + 1;
    
        % Find putative feature matches
        indexPairs = matchFeatures(preFeatures, currFeatures, Unique=matchUnique, MaxRatio=maxRatio, MatchThreshold=matchThreshold);
    
        preMatchedPoints = prePoints(indexPairs(:,1),:); % matched feature points
        currMatchedPoints = currPoints(indexPairs(:,2),:); % matched feature points
      
        if size(indexPairs, 1) < minMatches % num matched threshold
            continue 
        end
    
        % homography / fundamental matrix
        [tformH, scoreH, inliersIdxH] = compute_homography(preMatchedPoints, currMatchedPoints);
        [tformF, scoreF, inliersIdxF] = compute_fundamental_matrix(preMatchedPoints, currMatchedPoints);
    
        ratio = scoreH / (scoreH + scoreF);
        if ratio > ratioThreshold
            inlierTformIdx = inliersIdxH; tform = tformH;
        else
            inlierTformIdx = inliersIdxF; tform = tformF;
        end
    
        % relative pose (1/2 points)
        inlierPrePoints = preMatchedPoints(inlierTformIdx); % matched feature points inlier
        inlierCurrPoints = currMatchedPoints(inlierTformIdx); % matched feature points inlier
        [relPose, validFraction] = estrelpose(tform, intrinsics, inlierPrePoints(1:2:end), inlierCurrPoints(1:2:end));
    
        if validFraction < 0.9 || numel(relPose)==3 % threshold
            continue
        end
    
        % triangulation and compute 3d points
        [isValid, xyzWorldPoints, inlierTriangulationIdx] = compute_triangulation(rigidtform3d, relPose, inlierPrePoints, inlierCurrPoints, intrinsics, minParallax);
    
        if ~isValid % threshold
            continue
        end
    
        isMapInitialized = true;
        indexPairs = indexPairs(inlierTformIdx(inlierTriangulationIdx),:);
    end 

end


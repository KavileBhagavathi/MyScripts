% image = imread('totoro-starry-night-sky-thumb.jpg');
% imshow(image)
clc;
clear;

format("longG");
imgfileprefix = "imfileprefix."; %the scripts expects the images to have a common prefix
subdirectory = "subdirectory/"; %the script expects the images to be in a subdirectory. sample file path: subdirectory/imfileprefix.0001.png  
imgfiletype = ".png"; %change file extension if needed
% Prepare the new file.
vidObj = VideoWriter('dbM_CrDefDefDef.mp4','MPEG-4');
vidObj.FrameRate = 20; %set frame rate according to your need
open(vidObj);
for i = 1:300
    k = (i-1)*0.0001;
    req_numchar = num2str(sprintf('%.4f', k));
    req_str = extractAfter(req_numchar,".");
    img = imread(strcat(subdirectory,imgfileprefix,req_str,imgfiletype));
    frame = im2frame(img);
    writeVideo(vidObj,frame);
end
% Close the file.
close(vidObj);
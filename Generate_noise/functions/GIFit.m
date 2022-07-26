function [ ] = GIFit(folder, delay, outfilename, outdestination)
% Turns all files of below stated types in this folder into a gif
% This is a modified version of 
% image2animation.m by Moshe Lindner, Bar-Ilan University, Israel.
% Copyright (c) 2010, Moshe Lindner
% that is compatible with AVIit.m
% Supply:
%   1) input folder name (folder='.\foo';)
%   2) delay in seconds (delay=0.2;)
%   3) outfilename (outfilename='foo';)
%   4) optional: a directory for the created gif
%       (default: same as folder with individual images)
% File types:
types = [{'png'},{'jpg'},{'jpeg'},{'tiff'},{'tif'},{'bmp'},{'gif'}];
% Delay for first and last image:
delay1=delay;
delay2=delay; %all the same
% Number of loops:
loops=65535; % how often the gif will be played. This means "forever"
% loops=1;
% If no destination provided:
if ~exist('outdestination','var')
   outdestination = folder; 
end
% Create file name:
if ~strcmp(outfilename(end-2:end),'gif')
    outfilename = [outfilename '.gif'];
end
% Delete a previsouly generated gif to avoid including it again
moviefile=fullfile(outdestination,outfilename);
if exist(moviefile, 'file')
    delete(moviefile);
end
% Find files:
for ii=1:length(types)
    content = dir(fullfile(folder, ['*.' types{ii}]));
    temp = {content.name};
%     temp = temp(3:end); % cut off . and ..
    if ~exist('file_name','var')
        file_name=temp;
    else
        file_name = [file_name,temp];
    end
end
for i=1:length(file_name)
    if strcmpi('gif',file_name{i}(end-2:end))
        [M  c_map]=imread(fullfile(folder, file_name{i}));
    else
        a=imread(fullfile(folder, file_name{i}));
        [M  c_map]= rgb2ind(a,256);
    end
    if i==1
        imwrite(M,c_map,moviefile,'gif','LoopCount',loops,'DelayTime',delay1)
    elseif i==length(file_name)
        imwrite(M,c_map,moviefile,'gif','WriteMode','append','DelayTime',delay2)
    else
        imwrite(M,c_map,moviefile,'gif','WriteMode','append','DelayTime',delay)
    end
end
end

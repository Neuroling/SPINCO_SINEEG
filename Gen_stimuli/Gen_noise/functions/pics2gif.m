function pics2gif(files,outputname)
% Author: GFraga-Gonzalez 2022
% Desc: read a bunch of jpg files, convert to .avi and then to gif
% Input: 
%   files - list of .jpg file names (e.g., {'Picture1.jpg','Picture2.jpg'})
%   outputname - name of output gif file (e.g.,  'overview.gif')
% Output: a .gif file showing all input pics

%% Create a video (avi
aviname  = strrep(outputname,'.gif','.avi'); 
video = VideoWriter(aviname); %create the video object
open(video); %open the file for writing
for f = 1:length(files)
  I = imread(files{f}); %read the next image
  writeVideo(video,I); %write the image to file
end
close(video); %close the file

%% Convert to gif 
vrinfo = VideoReader(aviname);
filename = outputname;
vidFrames = read(vrinfo);
for n = 1:vrinfo.NumFrames
      [imind,cm] = rgb2ind(vidFrames(:,:,:,n),255);
      if n == 1
          imwrite(imind,cm,filename,'gif', 'Loopcount',inf);
      else
          imwrite(imind,cm,filename,'gif','WriteMode','append');
      end
end

% delete avi file 
delete aviname
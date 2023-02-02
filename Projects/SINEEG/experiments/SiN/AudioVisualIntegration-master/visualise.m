function visualise(Audio,Visual,FsAudio,FreqsVisual,OutVideoFileName,VisType,CMap,threshold,use_vidcodecs_comp,CircleSize,path2ffmpeg,FsVideo,blurAmount)
% this function takes in:
% Visual = vector or matrix of length t (dim 2) that will be converted to
% brightness values or some other type of presentation. This is assumed to be normalized to have a max value of 1.
% Audio = stays unchanged, will be merged with Visual time-series
% OutVideoFileName = name of the video file to output
% VisType  = type of visualization. As a function of the input we can
% change: 'brightness','bouncing','radius' (dynamic change of circle size).
% 'circleMulti' (multifreq presentation)
%
% CMap = choos any colormap term, e.g. 'gray' or 'copper'
% threshold = use a z-score threshold to identify peaks of the Visual input (in our case theta peaks)
% use_vidcodecs_comp = use video compression (mjpeg), true or false
% CircleSize = the FIX average size of the presented circle


% we fix the refresh rate of the avi output to 60 Hz
debug = 0;
% this assumes uncompressed audio, PCM, 16bit, signed, little-endian (linux architecture)
AudioCodec = 'pcm_s16le';

%VideoCodec = 'mjpeg';%'mjpeg'; %'libx265';
%VideoCodec = 'libx264'
%VideoCodec = 'msmpeg4v2'
% might be worth trying this one out
%VideoCodec = 'libx264';

% you can set the blur to zero, if you do not want it
%blurAmount = 0;

% vertical offset for bouncing condition, relative screen position (range of [0,1])
vert_offset = 0.6;

% standard params
if nargin < 6
    VisType = 'circleOnly';
    CMap = 'white';
    
    % z-score based threshold
    threshold = 2.7;
    debug = 0;
end

if nargin < 11
    path2ffmpeg= '/usr/local/bin/';%'C:\Users\becker\Documents\ffmpeg\bin\';
end


if isempty(threshold)
    binarize = false;
else
    binarize = true;
    
end

% if we only have a vector, we make a simple circle
if min(size(Visual))==1 & (strcmp(VisType,'bouncing') | strcmp(VisType,'radius') | strcmp(VisType,'brightness') )
    %if strcmp(VisType,'circle')
    
    %Visual = repmat(Visual,16,1);
    % this defines the circle for the 1D case
    t = linspace(0, 2*pi);
    
    % this defines size for circle
    r = CircleSize;
    X = r*cos(t);
    
    if  (strcmp(VisType,'bouncing'))
        % Y = r*sin(t) - r/2;
        Y = r*sin(t) - vert_offset + r/2;
    else
        Y = r*sin(t);
    end
    
    % if we have more info to display, we make circular polygons
else
    % this defines the dimension and units of the circle for the multidim case - the more
    % frequencies, the more fine-grained the dynamics
    xCoord = linspace(0,2*pi,size(Visual,1));
    yCoord = linspace(ceil(FreqsVisual(1)),ceil(FreqsVisual(end)),size(Visual,1));
    [TH,R] = meshgrid(xCoord,yCoord);
    [X,Y] = pol2cart(TH,R);
    contour_ticks = -0.5:0.05:7;
    debug=0;
    
end

%     figure(1)
%   patch(x, y, z)
vidObj = vision.VideoFileWriter(OutVideoFileName, 'AudioInputPort',true); %create the video object
vidObj.VideoCompressor='DV Video Encoder';
set(vidObj,'FrameRate',FsVideo);
FrameLength=round(FsAudio/vidObj.FrameRate);

% bit of rescaling
%Visual = zscore(Visual')';

% no negative values (not really necessary)
minVisual = min(Visual(:));
% This is not good, it removes the _desirable_ floor effects specified in
% call. Oups.
%Visual = Visual - minVisual;

% thresholding to binarize
% simplistic approach right now
%
% if binarize
%     tmp = zeros(size(Visual));
%     %tmp(find(Visual>threshold))=Visual(find(Visual>threshold));
%    tmp(find(Visual>threshold))=1;
%
%     Visual = tmp;
% end

if binarize
    % find peaks that are at least 150ms apart
    for chs = 1:size(Visual,2)
        [pks,locs] = findpeaks(Visual(:,chs),'MinPeakDistance',0.15/(1/FsVideo))
        tmp = zeros(size(Visual,1),1);
        for locsi = 1:length(locs)
            tmp(locs(locsi)-1:locs(locsi)+1)=1;
        end
        Visual(:,chs) = tmp;
    end
end

if size(Visual,2) == 1
    Visual =Visual';
end


% create the color / luminance gradients
for k=1:length(Visual)
    [Z(:,:,k)] = meshgrid((Visual(:,k)));
end

% only needed for smoothing the polygons
gausswinlr=gausswin(size(Z(:,:,1))*2);
gausswinr=gausswinlr(end/2+1:end);


for k=1:length(Visual)
    % we are not doing smoothing of the gradient (across frequencies) ATM
    % to create smooth polygons, so commented out
    %[Z_1D(:,:,k)] = meshgrid(Visual(:,k).*gausswinr);
    [Z_1D(:,:,k)] = meshgrid(Visual(:,k).*ones(size(Visual,1),1));
    
end

% for proper color scaling (NB: done globally!)
[MINMAX]=minmax(Z_1D(:)');
contour_ticks=linspace(MINMAX(1),MINMAX(2),150);

% init movie
h=figure();
h.Position=[100, 0, 720, 480]; % figure window size and position
h.PaperPosition=[0, 0, 720, 480];  % size of frames captured from figure and add to video file
h.InvertHardcopy='off'; % don't loose black background when calling print function

%set(h,'PaperPosition',[0,0,1,1],'Units','normalized','PaperSize',[1,1],'OuterPosition',[0.5,0.5,0.25,0.5]);

%h=figure('units','normalized','OuterPosition',[0.5,0.5,0.25,0.25]);
%h=figure('units','normalized','OuterPosition',[0,0,1,1]);


% init figure
if strcmp(VisType,'bouncing') | strcmp(VisType,'brightness')
    patch(X, Y, squeeze(Z_1D(:,:,1))');
    xlim([-1 1])
    ylim([-1 1])
    axis square
elseif strcmp(VisType,'radius')
    r = squeeze(Z_1D(:,:,1))';
    X = r*cos(t);
    Y = r*sin(t) %- r/2;
    patch(X, Y, 1);
    xlim([-1 1])
    ylim([-1 1])
    axis square
elseif strcmp(VisType,'circleMulti')
    contourf(X,Y,squeeze(Z_1D(:,:,1))',contour_ticks,'edgecolor','none');
    axis square
end

% the fix color limits we need to sensible plotting of envelope dynamics (across bands potentially)
%if sum(MINMAX)>0
%    set(gca, 'clim', [MINMAX(1) MINMAX(2)]);
%end
% some configuration params for the movie frames
if debug
    set(gca,'color',[1 1 1]);
    set(gcf,'color',[1 1 1]);
    colorbar
    axis on
else
    % we want it darker
    set(gca,'color',[0 0 0]);
    set(gcf,'color',[0 0 0]);
    axis off
end
axis tight manual
set(gca,'nextplot','replacechildren');
colormap(CMap);


NFrames=numel(1:FrameLength:(length(Audio)-FrameLength));


winsize=12;
kernel = (gausswin(winsize));
%Smoothing is now obsolete?

if (strcmp(VisType,'bouncing')) %|| (strcmp(VisType,'radius'))
    posit = squeeze(Z_1D(:,:,:))';
    posit_conv = conv(posit,kernel);
    posit_conv=posit_conv(winsize/2:end-winsize/2)*0.25;
else
    % dont do smoothing if not bouncing
    posit_conv = squeeze(Z_1D(:,:,:))';
end
% this goes through the envelope dynamics in time and creates one frame at
% a time, writes it to the file
%for k=1:length(Visual)
FrameNum = 1
for k=1:FrameLength:(length(Audio)-FrameLength)
    
    display(FrameNum);
    %figure(h); % don't refocus figure window
    
    if strcmp(VisType,'bouncing')
        %patch(X, Y+0, squeeze(Z_1D(:,:,FrameNum))');
        
        % has constant brightness of 1.
        patch(X, Y+posit_conv(FrameNum), 1);
        xlim([-1 1])
        ylim([-1 1])
        axis square
        
    elseif strcmp(VisType,'brightness')
        
        patch(X, Y, posit_conv(FrameNum));
        xlim([-1 1])
        ylim([-1 1])
        axis square
    elseif strcmp(VisType,'radius')
        r = posit_conv(FrameNum);
        X = r*cos(t);
        Y = r*sin(t);
        patch(X, Y, 1);
        xlim([-1 1])
        ylim([-1 1])
        axis square
    elseif strcmp(VisType,'circleMulti')
        contourf(X,Y,squeeze(Z_1D(:,:,FrameNum))',contour_ticks,'edgecolor','none');
        axis square
    end
    
    
    %set(gca, 'clim', [MINMAX(1) MINMAX(2)]);
    
    %if sum(MINMAX)>0
    %    set(gca, 'clim', [MINMAX(1) MINMAX(2)]);
    %end

    
    if (debug)
        colorbar;
    end
    % Write each frame to the file.
    currFrame = print(h,'-RGBImage','-r1'); % r1 means 1 dot per pixel (dpi but for rgb array)
    
    
    indices=[k:k+FrameLength-1];
    
    %don't forget to check whetehr you need to TRASNPOSE< because MATLAB is t3h suxx0rz
    %adding some blur to the circle using imgaussfilt
    if blurAmount >0
        step(vidObj,imgaussfilt(currFrame, blurAmount),squeeze(Audio(indices))'); % used to be currFrame.cdata
    else
        step(vidObj,currFrame,squeeze(Audio(indices))');
    end
    
    % after have written the video frame, reset circle to be black
    if strcmp(VisType,'bouncing')
        patch(X, Y+posit_conv(FrameNum), 0);
    elseif  strcmp(VisType,'brightness')
        patch(X, Y, 0);
    elseif strcmp(VisType,'radius')
        patch(X, Y, 0);
        
    end
    FrameNum = FrameNum +1;
    
    %writeVideo(vidObj,currFrame);
end

% Close the file.
% close(vidObj);

release(vidObj);


% this is for compression of combined AV files - makes a big difference...
% this needs ffmpeg to be installed, ideally on linux system, have not tried on other OS!
% use -y if you want to force overwrite
if use_vidcodecs_comp
    OutVideoFileNameComp = [OutVideoFileName(1:end-4) '.mkv'];
    system([path2ffmpeg 'ffmpeg -y -i ' OutVideoFileName ' -vcodec ' VideoCodec ...
      ' -preset ' 'veryslow' ' -x264-params ' 'crf=0'  ' -acodec ' AudioCodec ' ' OutVideoFileNameComp]);
      %' -acodec ' AudioCodec ' ' OutVideoFileNameComp]);

   % system([path2ffmpeg 'ffmpeg -y -i ' OutVideoFileName ' -vcodec ' VideoCodec '  -acodec ' AudioCodec ' ' OutVideoFileNameComp])
    
end








%%make the frames:






function audiowriteandscale(Filename,wave,Srate,MaxVal)
if MaxVal==0 %don't scale it
    audiowrite(Filename,wave,Srate); %
else
    max_sample=max(abs(wave));
    ratio=MaxVal/max_sample;
    wave=wave * ratio;
    audiowrite(Filename,wave,Srate);
end

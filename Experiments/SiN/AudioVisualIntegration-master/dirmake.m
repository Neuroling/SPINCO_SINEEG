%make directory if it doesn't already exist
function [varargout] = dirmake(targetpath)
if ~exist(targetpath,'dir')
    mkdir(targetpath)
end
if nargout==1
    varargout{1}=targetpath;
end

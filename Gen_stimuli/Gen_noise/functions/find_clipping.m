function [clipidx]= find_clipping(sigs, varargin)
% ==========================================================
%  Check if there is clipping in any signal 
% ==========================================================
%Author: G.FragaGonzalez 2022  
%Description
%  Just checks if a value exceeds +- 1 
%Usage:
%  Inputs 
%    sigs - a cell array with input audio signal vectors (e.g., after reading with audioread)  %   
%  Outputs 
%      clipidx - numeric index of the signals where a value was >1 or <-1
%%
clip_thresh = 1; 
checkmax = cellfun(@(x) max(x)>= clip_thresh, sigs,'UniformOutput',0);
checkmin = cellfun(@(x) min(x)<= -clip_thresh, sigs,'UniformOutput',0);
findclips = unique([find(cell2mat(checkmax)==1), find(cell2mat(checkmin)==1)]);

if isempty(findclips)
    %disp('...No clipping was found in any file')
    clipidx = 0;
else
   % disp(['clipping found in ', num2str(length(findclips)), ' sigs: ' num2str(findclips)])
    clipidx=findclips;
end 

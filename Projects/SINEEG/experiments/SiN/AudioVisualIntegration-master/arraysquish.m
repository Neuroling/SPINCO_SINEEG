function varargout=arraysquish(input,criterion,incexcFlag)
%%varargout=arraysquish(input,criterion,incexcFlag)
%This function will regexp through the input array to give you the output
%array that corresponds to the input criteria, or if you set the flag, the
%others
%if incexcFlag=1 then array is retained according to criterion, if
%incexcFlag=0 then it excluded according to criterion

indices=[find(cellfun(@isempty,regexp(input,criterion))~=incexcFlag)];
output=input(indices);
if isempty(output)
    output='';indices=[];
end
if nargout==1;
    varargout={output};
elseif nargout==2
    if ~isempty(indices)
    varargout=[{output}, indices];
    else
     varargout=[{output}, {indices}];
    end
end


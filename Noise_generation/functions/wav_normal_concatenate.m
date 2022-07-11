function [wavconcat] = wav_normal_concatenate(wavfiles)
% ==========================================================
%  Read and concatenate wav files
% ==========================================================
%Author: G.FragaGonzalez 2022 
%Description
%   Simply reads a list of wav files, scales them to the median rms and concatenates them 
%   Files must have the same sampling rate. 
%   If multiple channels are present, it will read one (and prompt warning)
%
%Usage:
%  Inputs 
%    wavfiles - cell with file names. e.g. {'sound1.wav','sound2.wav'}       
%   Outputs 
%    wavconcat - the concatenated signal of all files (as a row vector)

    % Check files are all .wav
    tmp = contains(wavfiles,'.wav','ignorecase',true);
    if (~isempty(find(tmp~=1,1))) 
        error('your input list must contain only .wav filenames !') 
    else 
        disp(['Reading ', num2str(length(wavfiles)),' files (.wav)...']);
    end

    % Read 
    amps = cell(length(wavfiles),1);
    frqs = cell(length(wavfiles),1);
    for i=1:length(wavfiles)        
        [amps{i},frqs{i}] = audioread(wavfiles{i});
        disp(wavfiles{i}) 
        
        if size(amps{i},2)>1 
            disp('Multiple channels in the file. Taking only the first') 
            tmp = amps{i};
            amps{i} = tmp(:,1);
        end
    end
    wavconcat = vertcat(amps{:});

    % Make it a row vector if not
    if ~isrow(wavconcat)
        wavconcat=wavconcat';
    end

    % CHECK: are sampling rates the same 
    if ~isempty(find(diff(cell2mat(frqs))~=0,1))
        clear wavconcat
        error ('sampling rates seem to differ!')
    end

end

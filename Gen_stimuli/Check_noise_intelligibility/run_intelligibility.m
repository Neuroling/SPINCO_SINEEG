clear all 
% Paths
dirinput_speech = 'V:\Projects\Spinco\SINEEG\Stimuli\AudioGens\tts-golang-44100hz\tts-golang-selected';
dirinput_sissn = 'V:\Projects\Spinco\SINEEG\Stimuli\AudioGens\tts-golang-44100hz\tts-golang-selected-SiSSN'; 
diroutput = 'V:\Projects\Spinco\SINEEG\Stimuli\AudioGens\tts-golang-44100hz' ;

cd (dirinput)
% find files
files_speech = dir([dirinput_speech,'\*.wav']);
files_speech = {files_speech.name};


tbl = table('Size', [0 4], 'VariableTypes', {'string', 'string','double', 'double'},'VariableNames', {'Folder','File', 'GP', 'DWGP'});
for fileinput = string(files_speech)
    % read ref signal
    [sig,fs] = audioread([dirinput_speech,'\',char(fileinput)]);
    ref = sig;      
    
    %find modified versions (SiSSN)
    files_mod = dir([dirinput_sissn,'\*',char(strrep(fileinput,'.wav','*.wav'))]);
    files_mod = {files_mod.name}; 
    
    for filemod =  string(files_mod)
        % read modified signal 
        [noise, fs] = audioread([dirinput_sissn,'\',char(filemod)]);
        % Get Glimps proportion measures     
        res = window_DWGP(sig,noise,fs);
        res2save = struct2table(rmfield(res, {'mask', 'rtv_mask','STEP_ref'}),"AsArray",true);
        res2save =  addvars(res2save,filemod,'NewVariableNames','File','Before',1);
        res2save =  addvars(res2save,string(dirinput_sissn),'NewVariableNames','Folder','Before',1);
        tbl = vertcat(tbl,res2save);      
    end           
end
%% get db info from filenames and add it to separate column
namesplit = split(tbl.File,'_');
namesplit = split(namesplit(:,5),'.wav');
tbl.SNR = namesplit(:,1); %add to original table 

% save table .tsv (tab delimited) 
writetable(tbl,[diroutput,'\sissn_intelligibility.csv'], 'Delimiter', ',');

%%%%%%%% info from main script used: 'window_DWGP'
%objscore = window_DWGP(sig, noise, fs, ref, presentationLevel)
% objscore = DWGP_LISTA(sig, ref, noise, fs) computes the distortion-weighted glimpse count
% indicating speech intelligibility in given noise signal.
%
% input:
%        sig           input modified speech signal
%        ref           input original speech signal
%        noise         input noise signal
%        fs            sampling frequency in Hz
%
% output:
%        objscore      objective scores in a structure: it returns both DWGP and original GP score.
%
% usage:
%        objscore = DWGP(sig, noise, fs, ref, presentationLevel);
%        If the input speech signal is a modified signal by any algorithm, the reference signal
%        should be the corresponding original/unmodified signal, otherwise the input speech and
%        reference speech signal should be identical. However if the duration of modified and
%        original signal is different, the modified speech itself will be always used as the
%        reference even if the original speech signal is supplied.
%
% Author: Yan Tang
% Date: 22.07.2012



clear ; close all; 
%% ========================================================================
%  Plot ERP topographies 
% ========================================================================
% Author: G.FragaGonzalez 2022
% Description
%  - Loads .set datasets and show topographical maps of activity using EEGlab
%  - Plots averaged activity along 3rd dimension (trials)
%  - Input files must contain channel location coordinates
%  - User defined time range to plot
%-------------------------------------------------------------------------
dirinput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_alpha';
diroutput = '/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/data_preproc_alpha/figs_topographies';
mkdir (diroutput)
cd(dirinput)

% User inputs 
times2plot = linspace(-1000,0,5); % in ms 
if length(times2plot)>6 
    error('STOP!  You want too many plots. Times to plot must be <= 6 !'); 
end

% look for src files 
files = dir([dirinput,'/*ICrem_alpha.set']);

%% Gather Group ERPs
[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
pop_editoptions( 'option_storedisk', 1); 
commands = {} % initialize 

 for f= 1:length(files)
        fileinput = files(f).name; 
        fileparts = strsplit(fileinput,'_')
        commands = {commands{:}...
            {'index' f 'load' [files(f).folder,'/',fileinput] 'subject' fileparts{1} }};
end 
[STUDY ALLEEG] = std_editset( STUDY, [], 'name','DiN','filename', 'DiN.study','commands',commands);
% Uncomment the line below to select ICA components with less than 15% residual variance
% commands = {commands{:} {'dipselect', 0.15}};

% Update workspace variables and redraw EEGLAB
CURRENTSTUDY = 1; EEG = ALLEEG; CURRENTSET = [1:length(EEG)];
[STUDY, ALLEEG] = std_checkset(STUDY, ALLEEG);
eeglab redraw         
             
 
end
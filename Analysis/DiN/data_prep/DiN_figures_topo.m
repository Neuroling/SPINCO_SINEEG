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

%% start file loop
groupEEG = {};
groupTrials = {};  
for f= 1:length(files)
    
    fileinput = files(f).name;
       
    % load file       
    EEG = pop_loadset('filename',fileinput,'filepath',dirinput); 
 
    %save in group array for later 
    groupEEG{f} = EEG.data;
    groupTrials{f} = [EEG.epoch.accuracy];

   %% Topography plots
   % plots
  figure;
  % loop thru correct/incorrect trials 
  accu = [0 1];  
  for a = 1:length(accu)
        
    % Average data  
    trials2use = find([EEG.epoch.accuracy]==accu(a));
    erpdata = mean(EEG.data(:,:,trials2use),3);
    
    % Fix range in mv 
    clim = [-1 1]; 

    % make plots
    for  t = 1:length(times2plot)   
           subplot(length(accu),length(times2plot),t+(length(times2plot)*(a-1)),'replace')
           timeidx = find(EEG.times == times2plot(t));
           topoplot(erpdata(:,timeidx),EEG.chanlocs,'electrodes', 'on','maplimits',clim,...
                              'headrad', 'rim','intsquare','off','style','fill','emarker',{'.','k',20,1})
          colormap(turbo(12))
          if t == 1 
              if accu(a)==1; accuStr = ['Correct Trials (','n = ',num2str(length(trials2use)),')'];
              else; accuStr = ['Incorrect Trials (','n = ',num2str(length(trials2use)),')'];
              end

              title({accuStr}, 'FontSize',16, 'FontName', 'calibri','fontweight','bold')
              subtitle([num2str(times2plot(t)) ' ms'], 'FontSize',14, 'FontName', 'calibri','fontweight','light')
          else
              subtitle([num2str(times2plot(t)) ' ms'], 'FontSize',14, 'FontName', 'calibri','fontweight','light')
          end  
    end 
        
   end
            
   % Adjust some common plot aesthetics
            sgtitle(strrep(fileinput,'_','\_'),'FontSize',16) 
            % aesthetics
            axis tight 
            CB = colorbar('Position',[0.9500 0.1100 0.015 0.1577], 'FontName','Calibri', 'FontSize', 12);                         
            % cbylab = get(CB,'YtickLabel'); 
            %cbylab{3,:}=  ['+',num2str(clim(2))];% add + to ylabels in colorbar
            % set (CB,'YTickLabel',cbylab); 
            cbpos = get(CB,'Position');
            %tit = get(gca,'Title');titpos=get(tit,'Position');
            %set(tit,'Position',[titpos(1) titpos(2)+0.01 titpos(3)]);    
            set(gcf, 'Position', get(0,'Screensize')); % Maximize figure
            set(gcf,'Color',[1 1 1] )  % white background   
  
    %% Save       
    cd(diroutput)
    saveas (gcf,['FigTopo_',strrep(fileinput,'.set','.jpg')],'jpg')        
    close gcf
end


%% Group plots
groupTs = horzcat(groupTrials{:});
groupDat = cat(3,groupEEG{:});
times = EEG.times ; % use times from any set opened before as ref
chanlocs = EEG.chanlocs;  %ditto
times2plot = linspace(-450,-50,5);
 figure;
  % loop thru correct/incorrect trials 
 
       
    % Average data  
    
    erpdata1 = mean(groupDat(:,:,find(groupTs==1)),3);
    erpdata2 = mean(groupDat(:,:,find(groupTs==0)),3);
    erpdata = erpdata1-erpdata2
    % Fix range in mv 
    clim = [-0.5 1.5]; 
    % make plots
    for  t = 1:length(times2plot)   
           subplot(1,length(times2plot),t)
           timeidx = find(times == times2plot(t));
           topoplot(erpdata(:,timeidx),chanlocs,'electrodes', 'on','maplimits',clim,...
                              'headrad', 'rim','intsquare','off','style','fill','emarker',{'.','k',20,1})
          colormap(turbo(12))
          if t == 1 
              title({'Diff corr-incorr'}, 'FontSize',16, 'FontName', 'calibri','fontweight','bold')
              subtitle([num2str(times2plot(t)) ' ms'], 'FontSize',14, 'FontName', 'calibri','fontweight','light')
          else
              subtitle([num2str(times2plot(t)) ' ms'], 'FontSize',14, 'FontName', 'calibri','fontweight','light')
          end  
    end 
         % Adjust some common plot aesthetics
            sgtitle(strrep(fileinput,'_','\_'),'FontSize',16) 
            % aesthetics
            axis tight 
            CB = colorbar('Position',[0.9500 0.1100 0.015 0.1577], 'FontName','Calibri', 'FontSize', 12);                         
            % cbylab = get(CB,'YtickLabel'); 
            %cbylab{3,:}=  ['+',num2str(clim(2))];% add + to ylabels in colorbar
            % set (CB,'YTickLabel',cbylab); 
            cbpos = get(CB,'Position');
            %tit = get(gca,'Title');titpos=get(tit,'Position');
            %set(tit,'Position',[titpos(1) titpos(2)+0.01 titpos(3)]);    
            set(gcf, 'Position', get(0,'Screensize')); % Maximize figure
            set(gcf,'Color',[1 1 1] )  % white background   
  
   
  %% 




  figure;
  % loop thru correct/incorrect trials 
  for a = 1:length(accu)
       
    % Average data  
    trials2use = find(groupTs==accu(a));
    erpdata = mean(groupDat(:,:,trials2use),3);
   
    % Fix range in mv 
    clim = [-1 0.5]; 
    % make plots
    for  t = 1:length(times2plot)   
           subplot(length(accu),length(times2plot),t+(length(times2plot)*(a-1)),'replace')
           timeidx = find(times == times2plot(t));
           topoplot(erpdata(:,timeidx),chanlocs,'electrodes', 'on','maplimits',clim,...
                              'headrad', 'rim','intsquare','off','style','fill','emarker',{'.','k',20,1})
          colormap(turbo(12))
          if t == 1 
              if accu(a)==1; accuStr = ['Correct Trials (','n = ',num2str(length(trials2use)),')'];
              else; accuStr = ['Incorrect Trials (','n = ',num2str(length(trials2use)),')'];
              end

              title({accuStr}, 'FontSize',16, 'FontName', 'calibri','fontweight','bold')
              subtitle([num2str(times2plot(t)) ' ms'], 'FontSize',14, 'FontName', 'calibri','fontweight','light')
          else
              subtitle([num2str(times2plot(t)) ' ms'], 'FontSize',14, 'FontName', 'calibri','fontweight','light')
          end  
    end 
        
   end
            
   % Adjust some common plot aesthetics
            sgtitle('Group ERP topographies','FontSize',16) 
            % aesthetics
            axis tight 
            CB = colorbar('Position',[0.9500 0.1100 0.015 0.1577], 'FontName','Calibri', 'FontSize', 12);                         
            % cbylab = get(CB,'YtickLabel'); 
            %cbylab{3,:}=  ['+',num2str(clim(2))];% add + to ylabels in colorbar
            % set (CB,'YTickLabel',cbylab); 
            cbpos = get(CB,'Position');
            %tit = get(gca,'Title');titpos=get(tit,'Position');
            %set(tit,'Position',[titpos(1) titpos(2)+0.01 titpos(3)]);    
            set(gcf, 'Position', get(0,'Screensize')); % Maximize figure
            set(gcf,'Color',[1 1 1] )  % white background   
function DiN_pt01_preprocess_segment03(thisPath, theseSbj)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Reads in the merged file obtained after preprocessing step 2.
% Fixes many issues related to missing and duplicate triggers.
% This required extensive manual work.
% Adds behavioural data to the epoch field of the EEG dataset.
%
% Inputs:
% - thisPath: path to original .raw files
% - theseSbj: vector of subject IDs to convert to .set format
%
% Preprocessing steps carried out:
% ... continuing from those from preprocessing section 1:
% 9. Check data consistency
% 10. Epoch
% 11. Reject noisy epochs
% 12. Remove trails with no response
% 13. Run ICA and reject non-brain components
%
% This function calls functions from the EEGLAB toolbox (Delorme & 
% Makeig, 2004) version 2020.0 (running under Matlab 2018b).
%
% trigger code legend:
% 'DIN2' = block start
% 'DI28' = block end
% 'DIN6' = stim onset digit 0
% 'DIN8' = stim onset digit 1
% 'DI10' = stim onset digit 2
% 'DI12' = stim onset digit 3
% 'DI14' = stim onset digit 4
% 'DI16' = stim onset digit 5
% 'DI18' = stim onset digit 6
% 'DI20' = stim onset digit 8
% 'DI22' = stim onset digit 9
% 'DI24' = comprehension response onset
% 'DI26' = clarity response onset
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


[ALLEEG, EEG, CURRENTSET, LASTCOM, ALLCOM] = eeglab;

nSbj = length(theseSbj);

for subject = 1:nSbj
    
    sbj = theseSbj(subject);
    disp(' ');
    disp('********************************************************');
    disp(['                   SUBJECT ' num2str(sbj)]);
    disp('********************************************************');
        
    sbjDir = [thisPath 'SUBJECT_' num2str(sbj) '/EEG_DATA/'];
    inDir = [sbjDir 'DOWNSAMPLED/'];
    outDirName = 'DiN_Zsc/';
    outDir = [inDir outDirName];
    mkdir(outDir);
    
    setname = ['sbj_' num2str(sbj) ...
        '_downsampled_merged.set'];
    
    EEG = pop_loadset('filename',setname,'filepath',inDir);
    
    
    
    
    
    %% 09) check data consistency
    disp('---------------------------------------------------------------')
    disp('--------------- CHECKING DATA CONSISTENCY ---------------------')
    disp('---------------------------------------------------------------')

       % UREVENT
    if sbj == 4
        epStart = 201;
        epEnd = 1267;
    elseif sbj == 5
        epStart = 197;
        epEnd = 1265;
    elseif sbj == 6
        epStart = 198;
        epEnd = 1258;
    elseif sbj == 7
        epStart = 197;
        epEnd = 1267;
    elseif sbj == 8
        epStart = 197;
        epEnd = 1270;
    elseif sbj == 9
        epStart = 199;
        epEnd = 1271;
    elseif sbj == 10
        epStart = 194;
        epEnd = 1261;
    elseif sbj == 11
        epStart = 197;
        epEnd = 1288;
    elseif sbj == 12
        epStart = 195;
        epEnd = 1268;
    elseif sbj == 13
        epStart = 198;
        epEnd = 1259;
    elseif sbj == 14
        epStart = 198;
        epEnd = 1267;
    elseif sbj == 15
        epStart = 207;
        epEnd = 1274;
    elseif sbj == 16
        epStart = 194;
        epEnd = 1259;
    elseif sbj == 17
        epStart = 198;
        epEnd = 1262;
    elseif sbj == 18
        epStart = 199;
        epEnd = 1266;
    elseif sbj == 19
        epStart = 198;
        epEnd = 1261;
    elseif sbj == 20
        epStart = 196;
        epEnd = 1271;
    elseif sbj == 21
        epStart = 197;
        epEnd = 1253;    
    elseif sbj == 22
        epStart = 195;
        epEnd = 1256; 
    elseif sbj == 23
        epStart = 199;
        epEnd = 1266; 
     elseif sbj == 24
        epStart = 199;
        epEnd = 1271;
    elseif sbj == 25
        epStart = 1;
        epEnd = 1068;
    elseif sbj == 26
        epStart = 197;
        epEnd = 1260;
    elseif sbj == 27
        epStart = 201;
        epEnd = 1269;
    elseif sbj == 28
        epStart = 199;
        epEnd = 1264;
    elseif sbj == 29
        epStart = 199;
        epEnd = 1258;
    elseif sbj == 30
        epStart = 203;
        epEnd = 1270;
    elseif sbj == 31
        epStart = 203;
        epEnd = 1266;
    elseif sbj == 32
        epStart = 1;
        epEnd = 1073;
    elseif sbj == 33
        epStart = 198;
        epEnd = 1261;
    elseif sbj == 35
        epStart = 196;
        epEnd = 1260;
    elseif sbj == 36
        epStart = 196;
        epEnd = 1266;
    elseif sbj == 37
        epStart = 194;
        epEnd = 1257;
    elseif sbj == 38
        epStart = 191;
        epEnd = 1243;
    end

    
    %% associate digit presented with trigger code
    digFromTrig_II = NaN([1 epEnd]);
    eventOnsetLatency = NaN([1 epEnd]);
    eventIndex = NaN([1 epEnd]);
    responseIndex = NaN([1 epEnd]);
    validTrial = NaN([1 length(EEG.urevent)]);
    validResponse = NaN([1 length(EEG.urevent)]);
    j = 0;
    for i = epStart:epEnd %evStart:evEnd
        eventOnsetLatency(i) = EEG.urevent(i).latency;
        theseEvents = EEG.urevent(i).type;
        if contains(theseEvents,'DIN6')
            digFromTrig_II(i) = 0;
        elseif contains(theseEvents,'DIN8')
            digFromTrig_II(i) = 1;
        elseif contains(theseEvents,'DI10')
            digFromTrig_II(i) = 2;
        elseif contains(theseEvents,'DI12')
            digFromTrig_II(i) = 3;
        elseif contains(theseEvents,'DI14')
            digFromTrig_II(i) = 4;
        elseif contains(theseEvents,'DI16')
            digFromTrig_II(i) = 5;
        elseif contains(theseEvents,'DI18')
            digFromTrig_II(i) = 6;
        elseif contains(theseEvents,'DI20')
            digFromTrig_II(i) = 8;
        elseif contains(theseEvents,'DI22')
            digFromTrig_II(i) = 9;
        end
        
        if ~isnan(digFromTrig_II(i))
            j = j + 1;
            eventIndex(i) = j;
            validTrial(i) = 1;
        end
    end
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % check if stimulus triggers are appropriately matched with
    % (comprehension) response triggers:
    id = find(~isnan(validTrial));
    R_I = NaN([1 length(id)]);
    for i = 1:length(id)-1 %epStart:epEnd
        nextEvents = {EEG.urevent(id(i)+1:id(i+1)).type};
%         disp(nextEvents{1})
        if sum(contains(nextEvents,'DI24')) > 0 %isnan(digFromTrig_II(i + 1))
            r_id = find(contains(nextEvents,'DI24'));
            R_I(i) = id(i) + r_id(1);
%             disp(num2str(R_I(i)))
        end
    end
    i = length(id);
    nextEvents = {EEG.urevent(id(i)+1:epEnd).type};
    if sum(contains(nextEvents,'DI24')) > 0 %isnan(digFromTrig_II(i + 1))
        r_id = find(contains(nextEvents,'DI24'));
        R_I(i) = id(i) + r_id(1);
    end
    
    
    R = R_I;
    Rna = find(isnan(R_I));
    l = find(Rna == 1);
    if ~isempty(l)
        Rna(l) = [];
    end
    R(Rna) = R(Rna-1) + 1;
    if ~isempty(l)
        R(1) = 1;
    end
    j = 0;
    for i = epStart:epEnd
        if ismember(i, R)
            j = j + 1;
            if ismember(i, R_I)
                responseIndex(i) = j;
                validResponse(i) = 1;
            end
        end
    end
    
    
    
    idxx = find(isnan(eventIndex));
    EVENT_INDEX = eventIndex;
    EVENT_INDEX(idxx) = [];
    
    eventsRecorded = struct();
    
    eventsRecorded.digID = digFromTrig_II;
    eventsRecorded.latency = eventOnsetLatency;
    
    ID = find(isnan(digFromTrig_II));
    
    eventsRecorded.digID(ID) = [];
    eventsRecorded.latency(ID) = [];
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    responseLatency = NaN([1 epEnd]);
    for i = epStart:epEnd
        theseEvents = EEG.urevent(i).type;
        if contains(theseEvents,'DI24')
            responseLatency(i) = EEG.urevent(i).latency;
        end
    end
    ID2 = find(isnan(responseLatency));
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    eventsRecorded.responseLatency = responseLatency;
    eventsRecorded.responseLatency(ID2) = [];
    
    
    %% load record of events recorded from PTB
    % This part required a lot of manual work consisting in visually
    % comparing triggers codes recorded from the amplifier with actual
    % digit identity. Some triggers are missing to start with and some were
    % removed when calling clean_artifacts
    
    behavDir = [BWD '/SUBJECT_' num2str(sbj) '/DiN/'];
    
    nBlocks = 6;
    
    DIGIT_ID = [];
    ITI = [];
    ACCURACY = [];
    DEGRAD_LVL_ORIG = [];
    %     DEGRAD_3_LVL = [];
    CLARITY_ORIG = [];
    %     CLARITY_3_LVL = [];
    
    for block = 1:nBlocks
        load([behavDir 'BLOCK_' num2str(block) '/SiN_block_' num2str(block) '_DATA.mat']); % [DATA]
        DIGIT_ID = [DIGIT_ID ; (cell2mat({DATA{:,9}}))'];
        ITI = [ITI ; (round(cell2mat({DATA{:,8}}),1))'];
        DEGRAD_LVL_ORIG = [DEGRAD_LVL_ORIG ; (cell2mat({DATA{:,11}}))'];
        ACCURACY = [ACCURACY ; (cell2mat({DATA{:,7}}))'];
        CLARITY_ORIG = [CLARITY_ORIG ; (cell2mat({DATA{:,5}}))'];
    end
    
    
    % I made a very silly function which creates groups according to
    % thirdtiles. Can be made much much simpler
    [CLARITYgroups,FORMULA,BOUNDARIES,CLARITY3lvls] = recodeCLARITY(CLARITY_ORIG);
    
    digID = DIGIT_ID;
    digFromTrig = (eventsRecorded.digID)';
    
    dif = length(digID) - length(digFromTrig);
    if dif > 0
        D = [digID [digFromTrig ; NaN([dif 1])]];
    elseif dif < 0
        D = [[digID ; NaN([abs(dif) 1])] digFromTrig];
    else
        D = [digID digFromTrig];
    end
    

    % MATCH STIMULUS TRIGGER CODES WITH PTB DATA:
    if sbj == 4
        digFromTrigAdj = [digFromTrig(1:3) ; NaN ; digFromTrig(4:end)];
        digFromTrigAdj = [digFromTrigAdj(1:65) ; NaN ; digFromTrigAdj(66:end)];
        digFromTrigAdj = [digFromTrigAdj(1:95) ; NaN ; digFromTrigAdj(96:end)];
        digFromTrigAdj = [digFromTrigAdj(1:104) ; digFromTrigAdj(106:end)];
        digFromTrigAdj = [digFromTrigAdj(1:153) ; NaN ;digFromTrigAdj(154:end)];
        digFromTrigAdj = [digFromTrigAdj(1:163) ; NaN ;digFromTrigAdj(164:end)];
        digFromTrigAdj = [digFromTrigAdj(1:190) ; NaN ;digFromTrigAdj(191:end)];
        digFromTrigAdj = [digFromTrigAdj(1:221) ; NaN ; NaN ;digFromTrigAdj(223:end)];
        digFromTrigAdj = [digFromTrigAdj(1:288) ; NaN ; NaN ;digFromTrigAdj(290:end)];
        digFromTrigAdj = [digFromTrigAdj(1:318) ; digFromTrigAdj(320:end)];
        digFromTrigAdj = [digFromTrigAdj(1:324) ; NaN ; digFromTrigAdj(325:end)];
    elseif sbj == 5
        digFromTrigAdj = [digFromTrig(1:46) ; NaN ; digFromTrig(47:end)];
        digFromTrigAdj = [digFromTrigAdj(1:63) ; NaN ; digFromTrigAdj(64:end)];
        digFromTrigAdj = [digFromTrigAdj(1:93) ; NaN ; digFromTrigAdj(94:end)];
        digFromTrigAdj = [digFromTrigAdj(1:151) ; NaN ; digFromTrigAdj(152:end)];
        digFromTrigAdj = [digFromTrigAdj(1:179) ; NaN ; digFromTrigAdj(180:end)];
        digFromTrigAdj = [digFromTrigAdj(1:203) ; NaN ; NaN ; digFromTrigAdj(205:end)];
        digFromTrigAdj = [digFromTrigAdj(1:211) ; digFromTrigAdj(213:end)];
        digFromTrigAdj = [digFromTrigAdj(1:219) ; digFromTrigAdj(221:end)];
        digFromTrigAdj = [digFromTrigAdj(1:231) ; NaN ; digFromTrigAdj(232:end)];
        digFromTrigAdj = [digFromTrigAdj(1:244) ; NaN ; NaN ; digFromTrigAdj(246:end)];
        digFromTrigAdj = [digFromTrigAdj(1:258) ; digFromTrigAdj(260:end)];
        digFromTrigAdj = [digFromTrigAdj(1:269) ; NaN ; digFromTrigAdj(270:end)];
        digFromTrigAdj = [digFromTrigAdj(1:301) ; digFromTrigAdj(303:end)];
        digFromTrigAdj = [digFromTrigAdj(1:306) ; digFromTrigAdj(308:end)];
        digFromTrigAdj = [digFromTrigAdj(1:310) ; NaN ; digFromTrigAdj(311:end)];
        digFromTrigAdj = [digFromTrigAdj(1:331) ; digFromTrigAdj(333:end)];
        digFromTrigAdj = [digFromTrigAdj(1:335) ; digFromTrigAdj(337:end)];
        digFromTrigAdj = [digFromTrigAdj(1:338) ; NaN ; digFromTrigAdj(339:end)];
        digFromTrigAdj = [digFromTrigAdj(1:347) ; digFromTrigAdj(349:end)];
        digFromTrigAdj = [digFromTrigAdj(1:352) ; NaN ; NaN ;digFromTrigAdj(353:end)];
        digFromTrigAdj = [digFromTrigAdj(1:375) ; digFromTrigAdj(377:end)];
    elseif sbj == 6
        digFromTrigAdj = [digFromTrig(1:10) ; NaN ; digFromTrig(11:end)];
        digFromTrigAdj = [digFromTrigAdj(1:18) ; NaN ; NaN ; digFromTrigAdj(20:end)];
        digFromTrigAdj = [digFromTrigAdj(1:41) ; NaN ; digFromTrigAdj(42:end)];
        digFromTrigAdj = [digFromTrigAdj(1:46) ; NaN ; digFromTrigAdj(47:end)];
        digFromTrigAdj = [digFromTrigAdj(1:64) ; digFromTrigAdj(66:end)];
        digFromTrigAdj = [digFromTrigAdj(1:85) ; digFromTrigAdj(87:end)];
        digFromTrigAdj = [digFromTrigAdj(1:100) ; NaN ; digFromTrigAdj(101:end)];
        digFromTrigAdj = [digFromTrigAdj(1:139) ; digFromTrigAdj(141:end)];
        digFromTrigAdj = [digFromTrigAdj(1:162) ; NaN ; digFromTrigAdj(163:end)];
        digFromTrigAdj = [digFromTrigAdj(1:228) ; NaN ; digFromTrigAdj(229:end)];
        digFromTrigAdj = [digFromTrigAdj(1:240) ; NaN ; digFromTrigAdj(241:end)];
        digFromTrigAdj = [digFromTrigAdj(1:259) ; NaN ; digFromTrigAdj(260:end)];
        digFromTrigAdj = [digFromTrigAdj(1:283) ; NaN ; digFromTrigAdj(284:end)];
        digFromTrigAdj = [digFromTrigAdj(1:299) ; digFromTrigAdj(301:end)];
        digFromTrigAdj = [digFromTrigAdj(1:322) ; NaN ; digFromTrigAdj(323:end)];
        digFromTrigAdj = [digFromTrigAdj(1:334) ; NaN ; digFromTrigAdj(335:end)];
        digFromTrigAdj = [digFromTrigAdj(1:348) ; NaN ; digFromTrigAdj(349:end)];
    elseif sbj == 7
        digFromTrigAdj = [digFromTrig(1:33) ; NaN ; NaN ; digFromTrig(35:end)];
        digFromTrigAdj = [digFromTrigAdj(1:45) ; NaN ; digFromTrigAdj(46:end)];
        digFromTrigAdj = [digFromTrigAdj(1:87) ; NaN ; NaN ; digFromTrigAdj(89:end)];
        digFromTrigAdj = [digFromTrigAdj(1:100) ; NaN ; digFromTrigAdj(101:end)];
        digFromTrigAdj = [digFromTrigAdj(1:116) ; digFromTrigAdj(118:end)];
        digFromTrigAdj = [digFromTrigAdj(1:121) ; digFromTrigAdj(123:end)];
        digFromTrigAdj = [digFromTrigAdj(1:146) ; digFromTrigAdj(148:end)];
        digFromTrigAdj = [digFromTrigAdj(1:150) ; digFromTrigAdj(152:end)];
        digFromTrigAdj = [digFromTrigAdj(1:162) ; NaN ; digFromTrigAdj(163:end)];
        digFromTrigAdj = [digFromTrigAdj(1:176) ; digFromTrigAdj(178:end)];
        digFromTrigAdj = [digFromTrigAdj(1:220) ; NaN ; digFromTrigAdj(221:end)];
        digFromTrigAdj = [digFromTrigAdj(1:258) ; NaN ; digFromTrigAdj(259:end)];
        digFromTrigAdj = [digFromTrigAdj(1:321) ; NaN ; digFromTrigAdj(322:end)];
        digFromTrigAdj = [digFromTrigAdj(1:346) ; digFromTrigAdj(348:end)];
    elseif sbj == 8
        digFromTrigAdj = [digFromTrig(1:11) ; NaN ; digFromTrig(12:end)];
        digFromTrigAdj = [digFromTrigAdj(1:40) ; digFromTrigAdj(42:end)];
        digFromTrigAdj = [digFromTrigAdj(1:105) ; NaN ; digFromTrigAdj(106:end)];
        digFromTrigAdj = [digFromTrigAdj(1:133) ; NaN ; digFromTrigAdj(134:end)];
        digFromTrigAdj = [digFromTrigAdj(1:229) ; NaN ; digFromTrigAdj(230:end)];
        digFromTrigAdj = [digFromTrigAdj(1:265) ; NaN ; digFromTrigAdj(266:end)];
        digFromTrigAdj = [digFromTrigAdj(1:288) ; NaN ; NaN ; digFromTrigAdj(290:end)];
        digFromTrigAdj = [digFromTrigAdj(1:317) ; digFromTrigAdj(319:end)];
        digFromTrigAdj = [digFromTrigAdj(1:344) ; NaN ; digFromTrigAdj(345:end)];
        digFromTrigAdj = [digFromTrigAdj(1:370) ; NaN ; digFromTrigAdj(371:end)];
    elseif sbj == 9
        digFromTrigAdj = [digFromTrig(1:16) ; NaN ; digFromTrig(17:end)];
        digFromTrigAdj = [digFromTrigAdj(1:42) ; digFromTrigAdj(44:end)];
        digFromTrigAdj = [digFromTrigAdj(1:142) ; NaN ; digFromTrigAdj(143:end)];
        digFromTrigAdj = [digFromTrigAdj(1:155) ; NaN ; digFromTrigAdj(156:end)];
        digFromTrigAdj = [digFromTrigAdj(1:182) ; digFromTrigAdj(184:end)];
        digFromTrigAdj = [digFromTrigAdj(1:214) ; digFromTrigAdj(216:end)];
        digFromTrigAdj = [digFromTrigAdj(1:247) ; digFromTrigAdj(249:end)];
        digFromTrigAdj = [digFromTrigAdj(1:295) ; NaN ; digFromTrigAdj(296:end)];
        digFromTrigAdj = [digFromTrigAdj(1:362) ; NaN ; digFromTrigAdj(363:end)];
    elseif sbj == 10
        digFromTrigAdj = [digFromTrig(1:2) ; NaN ; digFromTrig(3:end)];
        digFromTrigAdj = [digFromTrigAdj(1:13) ; NaN ; digFromTrigAdj(14:end)];
        digFromTrigAdj = [digFromTrigAdj(1:25) ; NaN ; digFromTrigAdj(26:end)];
        digFromTrigAdj = [digFromTrigAdj(1:30) ; NaN ; digFromTrigAdj(31:end)];
        digFromTrigAdj = [digFromTrigAdj(1:33) ; digFromTrigAdj(36:end)];
        digFromTrigAdj = [digFromTrigAdj(1:36) ; digFromTrigAdj(38:end)];
        digFromTrigAdj = [digFromTrigAdj(1:38) ; NaN ; NaN; NaN; digFromTrigAdj(41:end)];
        digFromTrigAdj = [digFromTrigAdj(1:74) ; NaN ; NaN; digFromTrigAdj(76:end)];
        digFromTrigAdj = [digFromTrigAdj(1:86) ; digFromTrigAdj(88:end)];
        digFromTrigAdj = [digFromTrigAdj(1:106) ; NaN ; digFromTrigAdj(107:end)];
        digFromTrigAdj = [digFromTrigAdj(1:139) ; NaN ; digFromTrigAdj(140:end)];
        digFromTrigAdj = [digFromTrigAdj(1:190) ; digFromTrigAdj(192:end)];
        digFromTrigAdj = [digFromTrigAdj(1:197) ; NaN ; digFromTrigAdj(198:end)];
        digFromTrigAdj = [digFromTrigAdj(1:241) ; digFromTrigAdj(243:end)];
        digFromTrigAdj = [digFromTrigAdj(1:320) ; NaN ; digFromTrigAdj(321:end)];
        digFromTrigAdj = [digFromTrigAdj(1:332) ; NaN ; digFromTrigAdj(333:end)];
        digFromTrigAdj = [digFromTrigAdj(1:345) ; NaN ; digFromTrigAdj(346:end)];
        digFromTrigAdj = [digFromTrigAdj(1:358) ; NaN ; digFromTrigAdj(359:end)];
        digFromTrigAdj = [digFromTrigAdj(1:372) ; NaN ; digFromTrigAdj(373:end)];
    elseif sbj == 11
        digFromTrigAdj = [digFromTrig(1) ; digFromTrig(3:end)];
        digFromTrigAdj = [digFromTrigAdj(1:5) ; NaN ; NaN ; digFromTrigAdj(7:end)];
        digFromTrigAdj = [digFromTrigAdj(1:25) ; digFromTrigAdj(31:end)];
        digFromTrigAdj = [digFromTrigAdj(1:29) ; NaN; NaN; digFromTrigAdj(31:end)];
        digFromTrigAdj = [digFromTrigAdj(1:41) ; NaN ; digFromTrigAdj(42:end)];
        digFromTrigAdj = [digFromTrigAdj(1:53) ; NaN ; digFromTrigAdj(54:end)];
        digFromTrigAdj = [digFromTrigAdj(1:117) ; NaN ; digFromTrigAdj(118:end)];
        digFromTrigAdj = [digFromTrigAdj(1:123) ; digFromTrigAdj(125:end)];
        digFromTrigAdj = [digFromTrigAdj(1:157) ; digFromTrigAdj(159:end)];
        digFromTrigAdj = [digFromTrigAdj(1:183) ; NaN ; digFromTrigAdj(184:end)];
        digFromTrigAdj = [digFromTrigAdj(1:191) ; digFromTrigAdj(193:end)];
        digFromTrigAdj = [digFromTrigAdj(1:238) ; NaN ; NaN; digFromTrigAdj(240:end)];
        digFromTrigAdj = [digFromTrigAdj(1:246) ; digFromTrigAdj(248:end)];
        digFromTrigAdj = [digFromTrigAdj(1:274) ; NaN ; digFromTrigAdj(275:end)];
        digFromTrigAdj = [digFromTrigAdj(1:277) ; digFromTrigAdj(279:end)];
        digFromTrigAdj = [digFromTrigAdj(1:315) ; digFromTrigAdj(317:end)];
        digFromTrigAdj = [digFromTrigAdj(1:326) ; digFromTrigAdj(328:end)];
        digFromTrigAdj = [digFromTrigAdj(1:342) ; digFromTrigAdj(344:end)];
        digFromTrigAdj = [digFromTrigAdj(1:346) ; digFromTrigAdj(348:end)];
        digFromTrigAdj = [digFromTrigAdj(1:351) ; NaN ; digFromTrigAdj(352:end)];
        digFromTrigAdj = [digFromTrigAdj(1:365) ; NaN ; digFromTrigAdj(366:end)];
        digFromTrigAdj = [digFromTrigAdj(1:368) ; digFromTrigAdj(370:end)];
        digFromTrigAdj = [digFromTrigAdj(1:374) ; digFromTrigAdj(376:end)];
    elseif sbj == 12
        digFromTrigAdj = [digFromTrig(1:31) ; digFromTrig(33:end)];
        digFromTrigAdj = [digFromTrigAdj(1:56) ; NaN ; digFromTrigAdj(57:end)];
        digFromTrigAdj = [digFromTrigAdj(1:66) ; digFromTrigAdj(68:end)];
        digFromTrigAdj = [digFromTrigAdj(1:79) ; NaN ; digFromTrigAdj(80:end)];
        digFromTrigAdj = [digFromTrigAdj(1:93) ; NaN ; digFromTrigAdj(94:end)];
        digFromTrigAdj = [digFromTrigAdj(1:103) ; digFromTrigAdj(105:end)];
        digFromTrigAdj = [digFromTrigAdj(1:123) ; NaN ; digFromTrigAdj(124:end)];
        digFromTrigAdj = [digFromTrigAdj(1:133) ; digFromTrigAdj(135:end)];
        digFromTrigAdj = [digFromTrigAdj(1:157) ; NaN ; digFromTrigAdj(158:end)];
        digFromTrigAdj = [digFromTrigAdj(1:198) ; NaN ; digFromTrigAdj(199:end)];
        digFromTrigAdj = [digFromTrigAdj(1:220) ; digFromTrigAdj(222:end)];
        digFromTrigAdj = [digFromTrigAdj(1:292) ; NaN ; NaN ;digFromTrigAdj(293:end)];
        digFromTrigAdj = [digFromTrigAdj(1:305) ; NaN ; NaN; digFromTrigAdj(306:end)];
        digFromTrigAdj = [digFromTrigAdj(1:321) ; NaN ; digFromTrigAdj(322:end)];
    elseif sbj == 13
        digFromTrigAdj = [digFromTrig(1:5) ;NaN;NaN; digFromTrig(7:end)];
        digFromTrigAdj = [digFromTrigAdj(1:36) ; NaN ; digFromTrigAdj(37:end)];
        digFromTrigAdj = [digFromTrigAdj(1:69) ; NaN ; digFromTrigAdj(70:end)];
        digFromTrigAdj = [digFromTrigAdj(1:82) ;NaN; digFromTrigAdj(83:end)];
        digFromTrigAdj = [digFromTrigAdj(1:99) ;NaN; digFromTrigAdj(100:end)];
        digFromTrigAdj = [digFromTrigAdj(1:112) ;NaN; digFromTrigAdj(113:end)];
        digFromTrigAdj = [digFromTrigAdj(1:123) ;NaN; digFromTrigAdj(124:end)];
        digFromTrigAdj = [digFromTrigAdj(1:165) ;NaN;NaN; digFromTrigAdj(167:end)];
        digFromTrigAdj = [digFromTrigAdj(1:177) ;NaN; digFromTrigAdj(178:end)];
        digFromTrigAdj = [digFromTrigAdj(1:187) ;NaN; digFromTrigAdj(188:end)];
        digFromTrigAdj = [digFromTrigAdj(1:223) ;NaN; digFromTrigAdj(224:end)];
        digFromTrigAdj = [digFromTrigAdj(1:235) ;NaN; digFromTrigAdj(236:end)];
        digFromTrigAdj = [digFromTrigAdj(1:257) ;NaN; digFromTrigAdj(258:end)];
        digFromTrigAdj = [digFromTrigAdj(1:268) ;NaN; digFromTrigAdj(269:end)];
        digFromTrigAdj = [digFromTrigAdj(1:279) ;NaN; digFromTrigAdj(280:end)];
        digFromTrigAdj = [digFromTrigAdj(1:292) ;NaN;NaN; digFromTrigAdj(293:end)];
        digFromTrigAdj = [digFromTrigAdj(1:306) ;NaN; digFromTrigAdj(307:end)];
        digFromTrigAdj = [digFromTrigAdj(1:337) ;NaN; digFromTrigAdj(338:end)];
        digFromTrigAdj = [digFromTrigAdj(1:377) ;NaN];
    elseif sbj == 14
        digFromTrigAdj = [digFromTrig(1:41) ; digFromTrig(43:end)];
        digFromTrigAdj = [digFromTrigAdj(1:57) ; digFromTrigAdj(59:end)];
        digFromTrigAdj = [digFromTrigAdj(1:59) ; NaN ; digFromTrigAdj(60:end)];
        digFromTrigAdj = [digFromTrigAdj(1:68) ; NaN ; digFromTrigAdj(69:end)];
        digFromTrigAdj = [digFromTrigAdj(1:112) ; NaN ; digFromTrigAdj(113:end)];
        digFromTrigAdj = [digFromTrigAdj(1:149) ; NaN ; digFromTrigAdj(150:end)];
        digFromTrigAdj = [digFromTrigAdj(1:151) ; digFromTrigAdj(153:end)];
        digFromTrigAdj = [digFromTrigAdj(1:187) ; NaN ; digFromTrigAdj(188:end)];
        digFromTrigAdj = [digFromTrigAdj(1:239) ; NaN ; NaN ; digFromTrigAdj(241:end)];
        digFromTrigAdj = [digFromTrigAdj(1:249) ; NaN ; NaN ;digFromTrigAdj(251:end)];
        digFromTrigAdj = [digFromTrigAdj(1:260) ; NaN ; digFromTrigAdj(261:end)];
        digFromTrigAdj = [digFromTrigAdj(1:310) ; NaN ; digFromTrigAdj(311:end)];
        digFromTrigAdj = [digFromTrigAdj(1:320) ; NaN ; digFromTrigAdj(321:end)];
        digFromTrigAdj = [digFromTrigAdj(1:355) ; digFromTrigAdj(357:end)];
        digFromTrigAdj = [digFromTrigAdj(1:360) ; digFromTrigAdj(362:end)];
        digFromTrigAdj = [digFromTrigAdj(1:366) ; digFromTrigAdj(368:end)];
    elseif sbj == 15
        digFromTrigAdj = [digFromTrig(1:6) ; digFromTrig(8:end)];
        digFromTrigAdj = [digFromTrigAdj(1:95); NaN ; digFromTrigAdj(96:end)];
        digFromTrigAdj = [digFromTrigAdj(1:124); NaN ; digFromTrigAdj(125:end)];
        digFromTrigAdj = [digFromTrigAdj(1:155); digFromTrigAdj(157:end)];
        digFromTrigAdj = [digFromTrigAdj(1:162); NaN ; digFromTrigAdj(163:end)];
        digFromTrigAdj = [digFromTrigAdj(1:165); digFromTrigAdj(167:end)];
        digFromTrigAdj = [digFromTrigAdj(1:172); NaN ; digFromTrigAdj(173:end)];
        digFromTrigAdj = [digFromTrigAdj(1:217); NaN ; digFromTrigAdj(218:end)];
        digFromTrigAdj = [digFromTrigAdj(1:252); digFromTrigAdj(254:end)];
        digFromTrigAdj = [digFromTrigAdj(1:324); NaN ; digFromTrigAdj(325:end)];
        digFromTrigAdj = [digFromTrigAdj(1:353); NaN ; digFromTrigAdj(354:end)];
        digFromTrigAdj = [digFromTrigAdj(1:372); digFromTrigAdj(374:end)];
    elseif sbj == 16
        digFromTrigAdj = [digFromTrig(1:19) ; NaN ; digFromTrig(20:end)];
        digFromTrigAdj = [digFromTrigAdj(1:29) ; NaN ; digFromTrigAdj(30:end)];
        digFromTrigAdj = [digFromTrigAdj(1:49) ; digFromTrigAdj(51:end)];
        digFromTrigAdj = [digFromTrigAdj(1:132) ; NaN ; digFromTrigAdj(133:end)];
        digFromTrigAdj = [digFromTrigAdj(1:153) ; NaN ; digFromTrigAdj(154:end)];
        digFromTrigAdj = [digFromTrigAdj(1:174) ; NaN ; digFromTrigAdj(175:end)];
        digFromTrigAdj = [digFromTrigAdj(1:190) ; digFromTrigAdj(192:end)];
        digFromTrigAdj = [digFromTrigAdj(1:232) ; digFromTrigAdj(234:end)];
        digFromTrigAdj = [digFromTrigAdj(1:260) ; NaN ; digFromTrigAdj(261:end)];
        digFromTrigAdj = [digFromTrigAdj(1:293) ; NaN ; digFromTrigAdj(294:end)];
        digFromTrigAdj = [digFromTrigAdj(1:305) ; NaN ; NaN; digFromTrigAdj(306:end)];
        digFromTrigAdj = [digFromTrigAdj(1:318) ; digFromTrigAdj(320:end)];
        digFromTrigAdj = [digFromTrigAdj(1:345) ; NaN ; digFromTrigAdj(346:end)];
        digFromTrigAdj = [digFromTrigAdj(1:354) ; NaN ; digFromTrigAdj(355:end)];
    elseif sbj == 17
        digFromTrigAdj = [digFromTrig(1:35) ;digFromTrig(37:end)];
        digFromTrigAdj = [digFromTrigAdj(1:50) ; NaN ; digFromTrigAdj(51:end)];
        digFromTrigAdj = [digFromTrigAdj(1:66) ; NaN ; digFromTrigAdj(67:end)];
        digFromTrigAdj = [digFromTrigAdj(1:148) ; NaN ; NaN ;digFromTrigAdj(150:end)];
        digFromTrigAdj = [digFromTrigAdj(1:159) ; NaN ; NaN ;digFromTrigAdj(161:end)];
        digFromTrigAdj = [digFromTrigAdj(1:183) ; NaN ; digFromTrigAdj(184:end)];
        digFromTrigAdj = [digFromTrigAdj(1:213) ; NaN ; digFromTrigAdj(214:end)];
        digFromTrigAdj = [digFromTrigAdj(1:224) ;digFromTrigAdj(226:end)];
        digFromTrigAdj = [digFromTrigAdj(1:264) ;NaN; digFromTrigAdj(265:end)];
        digFromTrigAdj = [digFromTrigAdj(1:287) ;NaN; digFromTrigAdj(288:end)];
        digFromTrigAdj = [digFromTrigAdj(1:299) ;NaN; digFromTrigAdj(300:end)];
        digFromTrigAdj = [digFromTrigAdj(1:303) ;digFromTrigAdj(305:end)];
        digFromTrigAdj = [digFromTrigAdj(1:333) ;NaN; NaN; digFromTrigAdj(335:end)];
        digFromTrigAdj = [digFromTrigAdj(1:348) ;NaN; NaN; digFromTrigAdj(350:end)];
        digFromTrigAdj = [digFromTrigAdj(1:360) ;NaN; digFromTrigAdj(361:end)];
    elseif sbj == 18
        digFromTrigAdj = [digFromTrig(1:59) ;NaN; digFromTrig(60:end)];
        digFromTrigAdj = [digFromTrigAdj(1:124) ; NaN ; digFromTrigAdj(125:end)];
        digFromTrigAdj = [digFromTrigAdj(1:147) ; NaN ; digFromTrigAdj(148:end)];
        digFromTrigAdj = [digFromTrigAdj(1:169) ; NaN ; digFromTrigAdj(170:end)];
        digFromTrigAdj = [digFromTrigAdj(1:179) ; NaN ; digFromTrigAdj(180:end)];
        digFromTrigAdj = [digFromTrigAdj(1:197) ; NaN ; digFromTrigAdj(198:end)];
        digFromTrigAdj = [digFromTrigAdj(1:218) ; NaN ;NaN;NaN; digFromTrigAdj(221:end)];
        digFromTrigAdj = [digFromTrigAdj(1:232) ; NaN ; digFromTrigAdj(233:end)];
        digFromTrigAdj = [digFromTrigAdj(1:258) ; digFromTrigAdj(260:end)];
        digFromTrigAdj = [digFromTrigAdj(1:260) ; NaN ; digFromTrigAdj(261:end)];
        digFromTrigAdj = [digFromTrigAdj(1:303) ; NaN ; digFromTrigAdj(304:end)];
        digFromTrigAdj = [digFromTrigAdj(1:348) ; NaN ; digFromTrigAdj(349:end)];
        digFromTrigAdj = [digFromTrigAdj(1:376) ; NaN ; NaN];
    elseif sbj == 19
        digFromTrigAdj = [digFromTrig(1:3) ; NaN ; digFromTrig(4:end)];
        digFromTrigAdj = [digFromTrigAdj(1:14) ; NaN ; digFromTrigAdj(15:end)];
        digFromTrigAdj = [digFromTrigAdj(1:25) ; NaN ; digFromTrigAdj(26:end)];
        digFromTrigAdj = [digFromTrigAdj(1:50) ; NaN ; digFromTrigAdj(51:end)];
        digFromTrigAdj = [digFromTrigAdj(1:62) ; NaN ; digFromTrigAdj(63:end)];
        digFromTrigAdj = [digFromTrigAdj(1:73) ; digFromTrigAdj(75:end)];
        digFromTrigAdj = [digFromTrigAdj(1:78) ; NaN ; digFromTrigAdj(79:end)];
        digFromTrigAdj = [digFromTrigAdj(1:108) ; digFromTrigAdj(110:end)];
        digFromTrigAdj = [digFromTrigAdj(1:140) ; digFromTrigAdj(142:end)];
        digFromTrigAdj = [digFromTrigAdj(1:153) ; NaN ; digFromTrigAdj(154:end)];
        digFromTrigAdj = [digFromTrigAdj(1:166) ; NaN ; NaN ; digFromTrigAdj(168:end)];
        digFromTrigAdj = [digFromTrigAdj(1:177) ; NaN ; digFromTrigAdj(178:end)];
        digFromTrigAdj = [digFromTrigAdj(1:189) ; NaN ; digFromTrigAdj(190:end)];
        digFromTrigAdj = [digFromTrigAdj(1:240) ; NaN ;NaN; digFromTrigAdj(242:end)];
        digFromTrigAdj = [digFromTrigAdj(1:289) ; NaN ; digFromTrigAdj(290:end)];
        digFromTrigAdj = [digFromTrigAdj(1:302) ; NaN ; digFromTrigAdj(303:end)];
        digFromTrigAdj = [digFromTrigAdj(1:329) ; digFromTrigAdj(331:end)];
        digFromTrigAdj = [digFromTrigAdj(1:343) ; digFromTrigAdj(345:end)];
        digFromTrigAdj = [digFromTrigAdj(1:347) ; NaN ; digFromTrigAdj(348:end)];
        digFromTrigAdj = [digFromTrigAdj(1:358) ; digFromTrigAdj(360:end)];
        digFromTrigAdj = [digFromTrigAdj(1:361) ; NaN ; digFromTrigAdj(362:end)];
        digFromTrigAdj = [digFromTrigAdj(1:375) ; NaN ; digFromTrigAdj(376:end)];
    elseif sbj == 20
        digFromTrigAdj = [digFromTrig(1:34) ; digFromTrig(36:end)];
        digFromTrigAdj = [digFromTrigAdj(1:49) ; NaN ; digFromTrigAdj(50:end)];
        digFromTrigAdj = [digFromTrigAdj(1:77) ; digFromTrigAdj(79:end)];
        digFromTrigAdj = [digFromTrigAdj(1:80) ; NaN; digFromTrigAdj(81:end)];
        digFromTrigAdj = [digFromTrigAdj(1:110) ; digFromTrigAdj(112:end)];
        digFromTrigAdj = [digFromTrigAdj(1:112) ; NaN; digFromTrigAdj(113:end)];
        digFromTrigAdj = [digFromTrigAdj(1:118) ; digFromTrigAdj(120:end)];
        digFromTrigAdj = [digFromTrigAdj(1:142) ; NaN;digFromTrigAdj(143:end)];
        digFromTrigAdj = [digFromTrigAdj(1:154) ; NaN; digFromTrigAdj(155:end)];
        digFromTrigAdj = [digFromTrigAdj(1:166) ; NaN;NaN; digFromTrigAdj(168:end)];
        digFromTrigAdj = [digFromTrigAdj(1:177) ; digFromTrigAdj(179:end)];
        digFromTrigAdj = [digFromTrigAdj(1:184) ; digFromTrigAdj(186:end)];
        digFromTrigAdj = [digFromTrigAdj(1:202) ;NaN; digFromTrigAdj(203:end)];
        digFromTrigAdj = [digFromTrigAdj(1:215) ;NaN; digFromTrigAdj(216:end)];
        digFromTrigAdj = [digFromTrigAdj(1:240) ;NaN;NaN; digFromTrigAdj(242:end)];
        digFromTrigAdj = [digFromTrigAdj(1:273) ; digFromTrigAdj(275:end)];
        digFromTrigAdj = [digFromTrigAdj(1:295) ; digFromTrigAdj(297:end)];
        digFromTrigAdj = [digFromTrigAdj(1:338) ;NaN;NaN; digFromTrigAdj(340:end)];
        digFromTrigAdj = [digFromTrigAdj(1:352) ;NaN; digFromTrigAdj(353:end)];
    elseif sbj == 21
        digFromTrigAdj = [digFromTrig(1) ; NaN ; digFromTrig(2:end)];
        digFromTrigAdj = [digFromTrigAdj(1:68) ; NaN ; digFromTrigAdj(69:end)];
        digFromTrigAdj = [digFromTrigAdj(1:81) ; NaN ; digFromTrigAdj(82:end)];
        digFromTrigAdj = [digFromTrigAdj(1:106) ; NaN ; digFromTrigAdj(107:end)];
        digFromTrigAdj = [digFromTrigAdj(1:163) ; NaN ; digFromTrigAdj(164:end)];
        digFromTrigAdj = [digFromTrigAdj(1:175) ; NaN ; digFromTrigAdj(176:end)];
        digFromTrigAdj = [digFromTrigAdj(1:187) ; NaN ;NaN; digFromTrigAdj(188:end)];
        digFromTrigAdj = [digFromTrigAdj(1:224) ; NaN ; digFromTrigAdj(225:end)];
        digFromTrigAdj = [digFromTrigAdj(1:251) ; NaN ; digFromTrigAdj(252:end)];
        digFromTrigAdj = [digFromTrigAdj(1:261) ; NaN ;NaN; digFromTrigAdj(263:end)];
        digFromTrigAdj = [digFromTrigAdj(1:287) ; NaN ; digFromTrigAdj(288:end)];
        digFromTrigAdj = [digFromTrigAdj(1:300) ; NaN ; digFromTrigAdj(301:end)];
        digFromTrigAdj = [digFromTrigAdj(1:314) ; NaN ; digFromTrigAdj(315:end)];
        digFromTrigAdj = [digFromTrigAdj(1:316) ; NaN ; digFromTrigAdj(317:end)];
        digFromTrigAdj = [digFromTrigAdj(1:329) ; NaN ; digFromTrigAdj(330:end)];
        digFromTrigAdj = [digFromTrigAdj(1:341) ;digFromTrigAdj(343:end)];
        digFromTrigAdj = [digFromTrigAdj(1:343) ; NaN ; digFromTrigAdj(344:end)];
        digFromTrigAdj = [digFromTrigAdj(1:348) ; digFromTrigAdj(350:end)];
        digFromTrigAdj = [digFromTrigAdj(1:371) ; NaN ; digFromTrigAdj(372:end)];
    elseif sbj == 22
        digFromTrigAdj = [digFromTrig(1:9);NaN;NaN;digFromTrig(11:end)];
        digFromTrigAdj = [digFromTrigAdj(1:17) ; digFromTrigAdj(19:end)];
        digFromTrigAdj = [digFromTrigAdj(1:19) ;NaN; digFromTrigAdj(20:end)];
        digFromTrigAdj = [digFromTrigAdj(1:42) ;NaN; digFromTrigAdj(43:end)];
        digFromTrigAdj = [digFromTrigAdj(1:54) ;NaN; digFromTrigAdj(55:end)];
        digFromTrigAdj = [digFromTrigAdj(1:76) ; digFromTrigAdj(78:end)];
        digFromTrigAdj = [digFromTrigAdj(1:88) ;NaN; digFromTrigAdj(89:end)];
        digFromTrigAdj = [digFromTrigAdj(1:98) ;NaN; digFromTrigAdj(99:end)];
        digFromTrigAdj = [digFromTrigAdj(1:104) ; digFromTrigAdj(106:end)];
        digFromTrigAdj = [digFromTrigAdj(1:135) ;NaN; digFromTrigAdj(136:end)];
        digFromTrigAdj = [digFromTrigAdj(1:169) ;NaN; digFromTrigAdj(170:end)];
        digFromTrigAdj = [digFromTrigAdj(1:181) ;NaN; digFromTrigAdj(182:end)];
        digFromTrigAdj = [digFromTrigAdj(1:188); digFromTrigAdj(190:end)];
        digFromTrigAdj = [digFromTrigAdj(1:191) ;NaN; digFromTrigAdj(192:end)];
        digFromTrigAdj = [digFromTrigAdj(1:201) ;NaN; digFromTrigAdj(202:end)];
        digFromTrigAdj = [digFromTrigAdj(1:212) ;NaN; digFromTrigAdj(213:end)];
        digFromTrigAdj = [digFromTrigAdj(1:228) ; digFromTrigAdj(230:end)];
        digFromTrigAdj = [digFromTrigAdj(1:256) ;NaN;NaN; digFromTrigAdj(258:end)];
        digFromTrigAdj = [digFromTrigAdj(1:302) ;NaN; digFromTrigAdj(303:end)];
        digFromTrigAdj = [digFromTrigAdj(1:314) ;NaN; digFromTrigAdj(315:end)];
        digFromTrigAdj = [digFromTrigAdj(1:324) ;NaN;NaN; digFromTrigAdj(326:end)];
        digFromTrigAdj = [digFromTrigAdj(1:328) ; digFromTrigAdj(330:end)];
        digFromTrigAdj = [digFromTrigAdj(1:337) ;NaN; digFromTrigAdj(338:end)];
        digFromTrigAdj = [digFromTrigAdj(1:341) ;digFromTrigAdj(343:end)];
        digFromTrigAdj = [digFromTrigAdj(1:348) ;NaN; digFromTrigAdj(349:end)];
    elseif sbj == 23
        digFromTrigAdj = [digFromTrig(1:52) ; NaN;NaN; digFromTrig(54:end)];
        digFromTrigAdj = [digFromTrigAdj(1:61) ; digFromTrigAdj(63:end)];
        digFromTrigAdj = [digFromTrigAdj(1:119) ;NaN;NaN; digFromTrigAdj(120:end)];
        digFromTrigAdj = [digFromTrigAdj(1:134) ; digFromTrigAdj(136:end)];
        digFromTrigAdj = [digFromTrigAdj(1:142) ; digFromTrigAdj(145:end)];
        digFromTrigAdj = [digFromTrigAdj(1:143) ;NaN;NaN;NaN;NaN; digFromTrigAdj(144:end)];
        digFromTrigAdj = [digFromTrigAdj(1:166) ;NaN;NaN; digFromTrigAdj(168:end)];
        digFromTrigAdj = [digFromTrigAdj(1:175) ; digFromTrigAdj(177:end)];
        digFromTrigAdj = [digFromTrigAdj(1:196) ; digFromTrigAdj(198:end)];
        digFromTrigAdj = [digFromTrigAdj(1:229) ;NaN; digFromTrigAdj(230:end)];
        digFromTrigAdj = [digFromTrigAdj(1:253) ;NaN; digFromTrigAdj(254:end)];
        digFromTrigAdj = [digFromTrigAdj(1:258) ; digFromTrigAdj(260:end)];
        digFromTrigAdj = [digFromTrigAdj(1:263) ;NaN; digFromTrigAdj(264:end)];
        digFromTrigAdj = [digFromTrigAdj(1:273) ; digFromTrigAdj(275:end)];
        digFromTrigAdj = [digFromTrigAdj(1:287) ; digFromTrigAdj(289:end)];
        digFromTrigAdj = [digFromTrigAdj(1:299) ;NaN; digFromTrigAdj(300:end)];
        digFromTrigAdj = [digFromTrigAdj(1:323) ;NaN; digFromTrigAdj(324:end)];
        digFromTrigAdj = [digFromTrigAdj(1:343) ; digFromTrigAdj(345:end)];
        digFromTrigAdj = [digFromTrigAdj(1:350) ;NaN;NaN;digFromTrigAdj(352:end)];
    elseif sbj == 24
        digFromTrigAdj = [digFromTrig(1:4) ; NaN ; digFromTrig(5:end)];
        digFromTrigAdj = [digFromTrigAdj(1:14) ; NaN ; digFromTrigAdj(15:end)];
        digFromTrigAdj = [digFromTrigAdj(1:29) ; digFromTrigAdj(31:end)];
        digFromTrigAdj = [digFromTrigAdj(1:118) ; digFromTrigAdj(120:end)];
        digFromTrigAdj = [digFromTrigAdj(1:135) ; NaN ;NaN; digFromTrigAdj(136:end)];
        digFromTrigAdj = [digFromTrigAdj(1:148) ; NaN;NaN; digFromTrigAdj(150:end)];
        digFromTrigAdj = [digFromTrigAdj(1:162) ; NaN ; digFromTrigAdj(163:end)];
        digFromTrigAdj = [digFromTrigAdj(1:187) ; NaN;NaN; digFromTrigAdj(188:end)];
        digFromTrigAdj = [digFromTrigAdj(1:196) ; NaN ; digFromTrigAdj(197:end)];
        digFromTrigAdj = [digFromTrigAdj(1:202) ; digFromTrigAdj(204:end)];
        digFromTrigAdj = [digFromTrigAdj(1:236) ; NaN ; digFromTrigAdj(237:end)];
        digFromTrigAdj = [digFromTrigAdj(1:273) ; NaN ; digFromTrigAdj(274:end)];
        digFromTrigAdj = [digFromTrigAdj(1:313) ; NaN ; digFromTrigAdj(314:end)];
        digFromTrigAdj = [digFromTrigAdj(1:341) ; NaN ; digFromTrigAdj(342:end)];
        digFromTrigAdj = [digFromTrigAdj(1:371)  ; digFromTrigAdj(373:end)];
    elseif sbj == 25
        digFromTrigAdj = [digFromTrig(1:13) ; NaN ; digFromTrig(14:end)];
        digFromTrigAdj = [digFromTrigAdj(1:24) ; NaN ; digFromTrigAdj(25:end)];
        digFromTrigAdj = [digFromTrigAdj(1:34) ; NaN;NaN;NaN; digFromTrigAdj(37:end)];
        digFromTrigAdj = [digFromTrigAdj(1:57) ; NaN ; digFromTrigAdj(58:end)];
        digFromTrigAdj = [digFromTrigAdj(1:115) ; NaN ; digFromTrigAdj(116:end)];
        digFromTrigAdj = [digFromTrigAdj(1:138) ; NaN ; digFromTrigAdj(139:end)];
        digFromTrigAdj = [digFromTrigAdj(1:143) ; digFromTrigAdj(145:end)];
        digFromTrigAdj = [digFromTrigAdj(1:161) ; NaN ; digFromTrigAdj(162:end)];
        digFromTrigAdj = [digFromTrigAdj(1:171) ; NaN ; digFromTrigAdj(172:end)];
        digFromTrigAdj = [digFromTrigAdj(1:202) ; NaN ; digFromTrigAdj(203:end)];
        digFromTrigAdj = [digFromTrigAdj(1:228) ; digFromTrigAdj(230:end)];
        digFromTrigAdj = [digFromTrigAdj(1:245) ; NaN ; digFromTrigAdj(246:end)];
        digFromTrigAdj = [digFromTrigAdj(1:248) ; digFromTrigAdj(250:end)];
        digFromTrigAdj = [digFromTrigAdj(1:258) ; NaN ; digFromTrigAdj(259:end)];
        digFromTrigAdj = [digFromTrigAdj(1:264) ; digFromTrigAdj(266:end)];
        digFromTrigAdj = [digFromTrigAdj(1:291) ; NaN ; digFromTrigAdj(292:end)];
        digFromTrigAdj = [digFromTrigAdj(1:302) ; NaN ; digFromTrigAdj(303:end)];
        digFromTrigAdj = [digFromTrigAdj(1:322) ; NaN ; digFromTrigAdj(323:end)];
        digFromTrigAdj = [digFromTrigAdj(1:333) ; NaN ;NaN; digFromTrigAdj(335:end)];
    elseif sbj == 26
        digFromTrigAdj = [digFromTrig(1:71) ; digFromTrig(73:end)];
        digFromTrigAdj = [digFromTrigAdj(1:82) ; NaN ; digFromTrigAdj(83:end)];
        digFromTrigAdj = [digFromTrigAdj(1:106) ; NaN ; digFromTrigAdj(107:end)];
        digFromTrigAdj = [digFromTrigAdj(1:111) ; NaN ; digFromTrigAdj(112:end)];
        digFromTrigAdj = [digFromTrigAdj(1:129) ; NaN ; digFromTrigAdj(130:end)];
        digFromTrigAdj = [digFromTrigAdj(1:143) ; NaN ; digFromTrigAdj(144:end)];
        digFromTrigAdj = [digFromTrigAdj(1:196) ; NaN ; digFromTrigAdj(197:end)];
        digFromTrigAdj = [digFromTrigAdj(1:238) ; NaN ; digFromTrigAdj(239:end)];
        digFromTrigAdj = [digFromTrigAdj(1:244) ; digFromTrigAdj(246:end)];
        digFromTrigAdj = [digFromTrigAdj(1:260) ; NaN ;NaN; digFromTrigAdj(261:end)];
        digFromTrigAdj = [digFromTrigAdj(1:274) ; NaN ; digFromTrigAdj(275:end)];
        digFromTrigAdj = [digFromTrigAdj(1:302) ; NaN ; digFromTrigAdj(303:end)];
        digFromTrigAdj = [digFromTrigAdj(1:345) ; NaN ;NaN; digFromTrigAdj(347:end)];
        digFromTrigAdj = [digFromTrigAdj(1:375) ; NaN ;NaN;NaN];
    elseif sbj == 27
        digFromTrigAdj = [digFromTrig(1:3) ; digFromTrig(5:end)];
        digFromTrigAdj = [digFromTrigAdj(1:37) ; NaN ; digFromTrigAdj(38:end)];
        digFromTrigAdj = [digFromTrigAdj(1:51) ; digFromTrigAdj(53:end)];
        digFromTrigAdj = [digFromTrigAdj(1:112) ; digFromTrigAdj(114:end)];
        digFromTrigAdj = [digFromTrigAdj(1:120) ;digFromTrigAdj(122:end)];
        digFromTrigAdj = [digFromTrigAdj(1:136) ; NaN ;NaN; digFromTrigAdj(138:end)];
        digFromTrigAdj = [digFromTrigAdj(1:173) ; NaN ;NaN; digFromTrigAdj(174:end)];
        digFromTrigAdj = [digFromTrigAdj(1:241) ; digFromTrigAdj(243:end)];
        digFromTrigAdj = [digFromTrigAdj(1:255) ; NaN ; digFromTrigAdj(256:end)];
        digFromTrigAdj = [digFromTrigAdj(1:286) ; digFromTrigAdj(288:end)];
        digFromTrigAdj = [digFromTrigAdj(1:290) ; NaN ; digFromTrigAdj(291:end)];
        digFromTrigAdj = [digFromTrigAdj(1:324) ; NaN ;NaN; digFromTrigAdj(326:end)];
        digFromTrigAdj = [digFromTrigAdj(1:327) ; digFromTrigAdj(329:end)];
    elseif sbj == 28
        digFromTrigAdj = [digFromTrig(1:12) ;NaN; digFromTrig(13:end)];
        digFromTrigAdj = [digFromTrigAdj(1:58) ; NaN ; digFromTrigAdj(59:end)];
        digFromTrigAdj = [digFromTrigAdj(1:71) ; digFromTrigAdj(73:end)];
        digFromTrigAdj = [digFromTrigAdj(1:72) ; digFromTrigAdj(74:end)];
        digFromTrigAdj = [digFromTrigAdj(1:79) ; NaN ; digFromTrigAdj(80:end)];
        digFromTrigAdj = [digFromTrigAdj(1:90) ; NaN ; digFromTrigAdj(91:end)];
        digFromTrigAdj = [digFromTrigAdj(1:110) ; digFromTrigAdj(112:end)];
        digFromTrigAdj = [digFromTrigAdj(1:122) ; digFromTrigAdj(124:end)];
        digFromTrigAdj = [digFromTrigAdj(1:132) ; NaN ; digFromTrigAdj(133:end)];
        digFromTrigAdj = [digFromTrigAdj(1:135) ; NaN ; digFromTrigAdj(136:end)];
        digFromTrigAdj = [digFromTrigAdj(1:158) ; digFromTrigAdj(160:end)];
        digFromTrigAdj = [digFromTrigAdj(1:161) ; digFromTrigAdj(164:end)];
        digFromTrigAdj = [digFromTrigAdj(1:168) ; NaN ; digFromTrigAdj(169:end)];
        digFromTrigAdj = [digFromTrigAdj(1:184) ; NaN ;NaN;NaN; digFromTrigAdj(187:end)];
        digFromTrigAdj = [digFromTrigAdj(1:230) ; digFromTrigAdj(232:end)];
        digFromTrigAdj = [digFromTrigAdj(1:235) ; NaN ; digFromTrigAdj(236:end)];
        digFromTrigAdj = [digFromTrigAdj(1:246) ; NaN ; digFromTrigAdj(247:end)];
        digFromTrigAdj = [digFromTrigAdj(1:268) ; NaN ; digFromTrigAdj(269:end)];
        digFromTrigAdj = [digFromTrigAdj(1:331) ; NaN ; digFromTrigAdj(332:end)];
        digFromTrigAdj = [digFromTrigAdj(1:369) ; NaN ;NaN;NaN; digFromTrigAdj(371:end)];
    elseif sbj == 29
        digFromTrigAdj = [digFromTrig(1:2) ; NaN ; digFromTrig(3:end)];
        digFromTrigAdj = [digFromTrigAdj(1:64) ; NaN ; digFromTrigAdj(65:end)];
        digFromTrigAdj = [digFromTrigAdj(1:78) ; digFromTrigAdj(80:end)];
        digFromTrigAdj = [digFromTrigAdj(1:87) ; digFromTrigAdj(89:end)];
        digFromTrigAdj = [digFromTrigAdj(1:97) ; NaN ; digFromTrigAdj(98:end)];
        digFromTrigAdj = [digFromTrigAdj(1:117) ; NaN ;NaN;NaN; digFromTrigAdj(119:end)];
        digFromTrigAdj = [digFromTrigAdj(1:132) ; NaN ; digFromTrigAdj(133:end)];
        digFromTrigAdj = [digFromTrigAdj(1:138) ; digFromTrigAdj(140:end)];
        digFromTrigAdj = [digFromTrigAdj(1:154) ; NaN ; digFromTrigAdj(155:end)];
        digFromTrigAdj = [digFromTrigAdj(1:195) ; NaN;NaN; digFromTrigAdj(196:end)];
        digFromTrigAdj = [digFromTrigAdj(1:218) ; NaN;NaN;NaN; digFromTrigAdj(221:end)];
        digFromTrigAdj = [digFromTrigAdj(1:226) ; NaN ; digFromTrigAdj(227:end)];
        digFromTrigAdj = [digFromTrigAdj(1:232) ; NaN ; digFromTrigAdj(233:end)];
        digFromTrigAdj = [digFromTrigAdj(1:244) ; NaN ; digFromTrigAdj(245:end)];
        digFromTrigAdj = [digFromTrigAdj(1:275) ; NaN ; digFromTrigAdj(276:end)];
        digFromTrigAdj = [digFromTrigAdj(1:292) ; digFromTrigAdj(294:end)];
        digFromTrigAdj = [digFromTrigAdj(1:338) ; NaN ;NaN; digFromTrigAdj(340:end)];
        digFromTrigAdj = [digFromTrigAdj(1:364) ; NaN ; digFromTrigAdj(365:end)];
        digFromTrigAdj = [digFromTrigAdj(1:376) ; NaN ; NaN];
    elseif sbj == 30
        digFromTrigAdj = [digFromTrig(1:26) ; digFromTrig(28:end)];
        digFromTrigAdj = [digFromTrigAdj(1:87) ; digFromTrigAdj(89:end)];
        digFromTrigAdj = [digFromTrigAdj(1:123) ; digFromTrigAdj(125:end)];
        digFromTrigAdj = [digFromTrigAdj(1:135) ;NaN; digFromTrigAdj(136:end)];
        digFromTrigAdj = [digFromTrigAdj(1:174) ;NaN; digFromTrigAdj(175:end)];
        digFromTrigAdj = [digFromTrigAdj(1:184) ;NaN;NaN;NaN; digFromTrigAdj(187:end)];
        digFromTrigAdj = [digFromTrigAdj(1:198) ;NaN; digFromTrigAdj(199:end)];
        digFromTrigAdj = [digFromTrigAdj(1:237) ;NaN; digFromTrigAdj(238:end)];
        digFromTrigAdj = [digFromTrigAdj(1:284) ;NaN;NaN; digFromTrigAdj(286:end)];
        digFromTrigAdj = [digFromTrigAdj(1:305) ; digFromTrigAdj(307:end)];
        digFromTrigAdj = [digFromTrigAdj(1:333) ;NaN;NaN; digFromTrigAdj(335:end)];
        digFromTrigAdj = [digFromTrigAdj(1:354) ; digFromTrigAdj(356:end)];
        digFromTrigAdj = [digFromTrigAdj(1:362) ;NaN;NaN; digFromTrigAdj(364:end)];
    elseif sbj == 31
        digFromTrigAdj = [digFromTrig(1:130) ; NaN ; digFromTrig(131:end)];
        digFromTrigAdj = [digFromTrigAdj(1:158) ; NaN ; digFromTrigAdj(159:end)];
        digFromTrigAdj = [digFromTrigAdj(1:178) ; digFromTrigAdj(180:end)];
        digFromTrigAdj = [digFromTrigAdj(1:222) ; NaN ;NaN; digFromTrigAdj(224:end)];
        digFromTrigAdj = [digFromTrigAdj(1:248) ; digFromTrigAdj(250:end)];
        digFromTrigAdj = [digFromTrigAdj(1:255) ; digFromTrigAdj(257:end)];
        digFromTrigAdj = [digFromTrigAdj(1:260) ; NaN;NaN; digFromTrigAdj(261:end)];
        digFromTrigAdj = [digFromTrigAdj(1:287) ; NaN ; digFromTrigAdj(288:end)];
        digFromTrigAdj = [digFromTrigAdj(1:326) ;NaN;NaN; digFromTrigAdj(327:end)];
        digFromTrigAdj = [digFromTrigAdj(1:341) ; NaN ; digFromTrigAdj(342:end)];
        digFromTrigAdj = [digFromTrigAdj(1:355) ; NaN ;NaN; digFromTrigAdj(357:end)];
        digFromTrigAdj = [digFromTrigAdj(1:362) ; NaN ;NaN; digFromTrigAdj(364:end)];
        digFromTrigAdj = [digFromTrigAdj(1:369) ; digFromTrigAdj(371:end)];
    elseif sbj == 32
        digFromTrigAdj = [digFromTrig(1:4) ; digFromTrig(6:end)];
        digFromTrigAdj = [digFromTrigAdj(1:51) ; NaN ; digFromTrigAdj(52:end)];
        digFromTrigAdj = [digFromTrigAdj(1:109) ; NaN ; digFromTrigAdj(110:end)];
        digFromTrigAdj = [digFromTrigAdj(1:118) ; digFromTrigAdj(120:end)];
        digFromTrigAdj = [digFromTrigAdj(1:130) ; digFromTrigAdj(132:end)];
        digFromTrigAdj = [digFromTrigAdj(1:177) ; NaN ; digFromTrigAdj(178:end)];
        digFromTrigAdj = [digFromTrigAdj(1:194) ; digFromTrigAdj(196:end)];
        digFromTrigAdj = [digFromTrigAdj(1:199) ; NaN ; digFromTrigAdj(200:end)];
        digFromTrigAdj = [digFromTrigAdj(1:224) ; NaN ; digFromTrigAdj(225:end)];
        digFromTrigAdj = [digFromTrigAdj(1:247) ; digFromTrigAdj(249:end)];
        digFromTrigAdj = [digFromTrigAdj(1:250) ; NaN ; digFromTrigAdj(251:end)];
        digFromTrigAdj = [digFromTrigAdj(1:292) ; digFromTrigAdj(294:end)];
        digFromTrigAdj = [digFromTrigAdj(1:337) ; NaN ; digFromTrigAdj(338:end)];
        digFromTrigAdj = [digFromTrigAdj(1:376) ; NaN ; NaN];
    elseif sbj == 33
        digFromTrigAdj = [digFromTrig(1:11) ; digFromTrig(13:end)];
        digFromTrigAdj = [digFromTrigAdj(1:79) ; NaN ; digFromTrigAdj(80:end)];
        digFromTrigAdj = [digFromTrigAdj(1:138) ; digFromTrigAdj(140:end)];
        digFromTrigAdj = [digFromTrigAdj(1:148) ; NaN;NaN;NaN; digFromTrigAdj(150:end)];
        digFromTrigAdj = [digFromTrigAdj(1:163) ;NaN; digFromTrigAdj(164:end)];
        digFromTrigAdj = [digFromTrigAdj(1:266) ; NaN ; digFromTrigAdj(267:end)];
        digFromTrigAdj = [digFromTrigAdj(1:291) ; NaN ;NaN; digFromTrigAdj(293:end)];
        digFromTrigAdj = [digFromTrigAdj(1:331) ; NaN ; digFromTrigAdj(332:end)];
    elseif sbj == 35
        digFromTrigAdj = [digFromTrig(1:8) ; NaN; digFromTrig(9:end)];
        digFromTrigAdj = [digFromTrigAdj(1:22) ; NaN ; digFromTrigAdj(23:end)];
        digFromTrigAdj = [digFromTrigAdj(1:70) ; NaN ; digFromTrigAdj(71:end)];
        digFromTrigAdj = [digFromTrigAdj(1:106) ; NaN ; digFromTrigAdj(107:end)];
        digFromTrigAdj = [digFromTrigAdj(1:120) ; NaN ; digFromTrigAdj(121:end)];
        digFromTrigAdj = [digFromTrigAdj(1:158) ; digFromTrigAdj(160:end)];
        digFromTrigAdj = [digFromTrigAdj(1:161) ; NaN ; digFromTrigAdj(162:end)];
        digFromTrigAdj = [digFromTrigAdj(1:173) ; NaN ; digFromTrigAdj(174:end)];
        digFromTrigAdj = [digFromTrigAdj(1:198) ; NaN ; digFromTrigAdj(199:end)];
        digFromTrigAdj = [digFromTrigAdj(1:235) ; digFromTrigAdj(237:end)];
        digFromTrigAdj = [digFromTrigAdj(1:262) ; digFromTrigAdj(264:end)];
        digFromTrigAdj = [digFromTrigAdj(1:309) ; NaN ; digFromTrigAdj(310:end)];
        digFromTrigAdj = [digFromTrigAdj(1:315) ; digFromTrigAdj(317:end)];
        digFromTrigAdj = [digFromTrigAdj(1:346) ; NaN;NaN; digFromTrigAdj(348:end)];
        digFromTrigAdj = [digFromTrigAdj(1:374) ; NaN ; digFromTrigAdj(375:end)];
    elseif sbj == 36
        digFromTrigAdj = [digFromTrig(1:12) ; digFromTrig(14:end)];
        digFromTrigAdj = [digFromTrigAdj(1:14) ;NaN; digFromTrigAdj(15:end)];
        digFromTrigAdj = [digFromTrigAdj(1:25) ;NaN; digFromTrigAdj(26:end)];
        digFromTrigAdj = [digFromTrigAdj(1:86) ; digFromTrigAdj(88:end)];
        digFromTrigAdj = [digFromTrigAdj(1:86) ; digFromTrigAdj(88:end)];
        digFromTrigAdj = [digFromTrigAdj(1:92) ;NaN; digFromTrigAdj(93:end)];
        digFromTrigAdj = [digFromTrigAdj(1:123) ; digFromTrigAdj(125:end)];
        digFromTrigAdj = [digFromTrigAdj(1:153) ;NaN; digFromTrigAdj(154:end)];
        digFromTrigAdj = [digFromTrigAdj(1:176) ;NaN;NaN; digFromTrigAdj(178:end)];
        digFromTrigAdj = [digFromTrigAdj(1:208) ; digFromTrigAdj(210:end)];
        digFromTrigAdj = [digFromTrigAdj(1:248) ;NaN;NaN; digFromTrigAdj(250:end)];
        digFromTrigAdj = [digFromTrigAdj(1:266) ; digFromTrigAdj(268:end)];
        digFromTrigAdj = [digFromTrigAdj(1:280) ;NaN;NaN; digFromTrigAdj(282:end)];
        digFromTrigAdj = [digFromTrigAdj(1:291) ;NaN; digFromTrigAdj(292:end)];
        digFromTrigAdj = [digFromTrigAdj(1:301) ; digFromTrigAdj(303:end)];
        digFromTrigAdj = [digFromTrigAdj(1:304) ;NaN; digFromTrigAdj(305:end)];
        digFromTrigAdj = [digFromTrigAdj(1:315) ;NaN; digFromTrigAdj(316:end)];
        digFromTrigAdj = [digFromTrigAdj(1:336) ; digFromTrigAdj(338:end)];
        digFromTrigAdj = [digFromTrigAdj(1:342) ;NaN; digFromTrigAdj(343:end)];
    elseif sbj == 37
        digFromTrigAdj = [digFromTrig(1:64) ; NaN ; digFromTrig(65:end)];
        digFromTrigAdj = [digFromTrigAdj(1:110) ; NaN ; digFromTrigAdj(111:end)];
        digFromTrigAdj = [digFromTrigAdj(1:118) ; digFromTrigAdj(120:end)];
        digFromTrigAdj = [digFromTrigAdj(1:129) ; NaN ;NaN; digFromTrigAdj(131:end)];
        digFromTrigAdj = [digFromTrigAdj(1:138) ; digFromTrigAdj(140:end)];
        digFromTrigAdj = [digFromTrigAdj(1:178) ; NaN ; digFromTrigAdj(179:end)];
        digFromTrigAdj = [digFromTrigAdj(1:201) ; NaN ; digFromTrigAdj(202:end)];
        digFromTrigAdj = [digFromTrigAdj(1:242) ; digFromTrigAdj(244:end)];
        digFromTrigAdj = [digFromTrigAdj(1:252) ; NaN ; digFromTrigAdj(253:end)];
        digFromTrigAdj = [digFromTrigAdj(1:315) ; NaN ; digFromTrigAdj(316:end)];
        digFromTrigAdj = [digFromTrigAdj(1:328) ; NaN ; digFromTrigAdj(329:end)];
        digFromTrigAdj = [digFromTrigAdj(1:353) ; digFromTrigAdj(355:end)];
        digFromTrigAdj = [digFromTrigAdj(1:354) ; NaN ; digFromTrigAdj(355:end)];
    elseif sbj == 38
        digFromTrigAdj = [digFromTrig(1:12) ; digFromTrig(14:end)];
        digFromTrigAdj = [digFromTrigAdj(1:16) ; NaN ; digFromTrigAdj(17:end)];
        digFromTrigAdj = [digFromTrigAdj(1:39) ; NaN ; digFromTrigAdj(40:end)];
        digFromTrigAdj = [digFromTrigAdj(1:85) ;NaN;NaN; digFromTrigAdj(86:end)];
        digFromTrigAdj = [digFromTrigAdj(1:97) ;NaN; digFromTrigAdj(98:end)];
        digFromTrigAdj = [digFromTrigAdj(1:109) ;NaN;NaN; digFromTrigAdj(110:end)];
        digFromTrigAdj = [digFromTrigAdj(1:147) ;NaN; digFromTrigAdj(148:end)];
        digFromTrigAdj = [digFromTrigAdj(1:174) ;NaN; digFromTrigAdj(175:end)];
        digFromTrigAdj = [digFromTrigAdj(1:189) ;NaN;NaN; digFromTrigAdj(190:end)];
        digFromTrigAdj = [digFromTrigAdj(1:215) ;NaN; digFromTrigAdj(216:end)];
        digFromTrigAdj = [digFromTrigAdj(1:241) ; digFromTrigAdj(243:end)];
        digFromTrigAdj = [digFromTrigAdj(1:324) ;NaN;NaN; digFromTrigAdj(326:end)];
        digFromTrigAdj = [digFromTrigAdj(1:338) ;NaN;NaN; digFromTrigAdj(340:end)];
        digFromTrigAdj = [digFromTrigAdj(1:354) ;NaN; digFromTrigAdj(355:end)];
        digFromTrigAdj = [digFromTrigAdj(1:357) ;NaN; digFromTrigAdj(358:end)];
        digFromTrigAdj = [digFromTrigAdj(1:374) ;NaN; digFromTrigAdj(375:end)];
    end

    % sanity check: dif must be equal to 0
    % dif = length(digID) - length(digFromTrigAdj);
    % if dif > 0
    %     D = [digID [digFromTrigAdj ; NaN([dif 1])]];
    % elseif dif < 0
    %     D = [[digID ; NaN([abs(dif) 1])] digFromTrigAdj];
    % else
    %     D = [digID digFromTrigAdj];
    % end

            tIDX = trialIDX;
        g  = find(isnan(trialIDX));
        tIDX(g) = 1;
        gdiff = length(digFromTrig) - length(tIDX);
        if gdiff > 0
            E = [[digID(tIDX) ; NaN([gdiff 1])] digFromTrig ];
        else
            E = [digID(tIDX) [digFromTrig ; NaN([abs(gdiff) 1])]];
        end
    
    %
    if sbj == 4
        trialIDX = [1:3 5:65 67:95 97:104 NaN 105:153 155:163 165:190 192:221 NaN ...
            224:288 NaN 291:318 NaN 319:324 326:378];
        missingIDX = [4 66 96 154 164 191 325];
        extraIDX = [105 319];
    elseif sbj == 5
        trialIDX = [1:46 48:63 65:93 95:151 153:179 181:203 205:211 NaN 212:219 ...
            NaN 220:231 233:244 247:258 NaN 259:269 271:301 NaN 302:306 NaN ...
            307:310 312:331 NaN 332:335 NaN 336:338 340:347 NaN 348:352 354:375 ...
            NaN 376:378];
        missingIDX = [47 64 94 152 180 204 232 245 246 270 311 339 353];
        extraIDX = [212 220 259 302 307 332 336 348 376]; %259 
    elseif sbj == 6
        trialIDX = [1:10 12:18 NaN 21:41 43:46 48:64 NaN 65:85 NaN 86:100 ...
            102:139 NaN 140:162 164:228 230:240 242:259 261:283 285:299 NaN ...
            300:322 324:334 336:348 350:378];
        missingIDX = [11 42 47 163 229 241 260 284 323 335 349];
        extraIDX = [65 86 140 300];
    elseif sbj == 7
        trialIDX = [1:33 NaN 36:45 47:87 NaN 90:100 102:116 NaN 117:121 NaN ...
            122:146 NaN 147:150 NaN 151:162 164:176 NaN 177:220 222:258 ...
            260:321 323:346 NaN 347:378];
        missingIDX = [46 101 163 221 259 322];
        extraIDX = [117 122 147 151 177 347];
    elseif sbj == 8
         trialIDX = [1:11 13:40 NaN 41:105 107:133 135:229 231:265 267:288 ...
             NaN 291:317 NaN 318:344 346:370 372:378]; 
         missingIDX = [12 106 134 230 266 345 371];
        extraIDX = [41 318];
    elseif sbj == 9
        trialIDX = [1:16 18:42 NaN 43:142 144:155 157:182 NaN 183:214 NaN 215:247 ...
            NaN 248:295 297:362 364:378];
        missingIDX = [17 143 156 296 363];
        extraIDX = [42 183 215 248];
    elseif sbj == 10
        trialIDX = [1 2 4:13 15:25 27:30 32 33 NaN NaN 34:36 ...
            NaN 37 38 NaN NaN 42:74 76:86 NaN 87:106 108:139 ...
            141:190 NaN 191:197 199:241 NaN 242:320 322:332 ...
            334:345 347:358 360:372 374:378];
        missingIDX = [3 14 26 31 75 107 198 321 333 346 359 373];
        extraIDX = [34 37 87 191 242];
    elseif sbj == 11
        trialIDX = [1 NaN 2:5 7:25 NaN NaN NaN NaN NaN 26:29 31:41 43:53 ...
            55:81 83:88 NaN 89:117 119:123 NaN 124:157 NaN 158:183 185:191 ...
            NaN 192:238 240:246 NaN 247:274 276:277 NaN 278:315 NaN 316:326 ...
            NaN 327:342 NaN 343:346 NaN 347:351 353:365 367:368 NaN 369:374 ...
            NaN 375:378];
        missingIDX = [6 30 42 54 82 118 184 239 275 352 366];
        extraIDX = [2 89 124 158 192 247 278 316 327 343 347 369 375];
    elseif sbj == 12
        trialIDX = [1:31 NaN 32:56 58:66 NaN 67:79 81:93 95:103 NaN 104:123 ...
            125:133 NaN 134:157 159:198 200:220 NaN 221:292 295:305 308:321 323:378];
        missingIDX = [57 80 94 124 158 199 293 294 306 307 322];
        extraIDX = [32 67 104 134 221];
    elseif sbj == 13
        trialIDX = [1:5 NaN 8:36 38:69 71:82 84:99 101:112 114:123 125:165 NaN ...
            168:177 179:187 189:223 225:235 237:257 259:268 270:279 281:292 ...
            295:306 308:337 339:376 377 NaN 378];
        missingIDX = [37 70 83 100 113 124 178 188 224 236 258 269 280 293 294 307 ...
            338 375];
        extraIDX = [378];
    elseif sbj == 14
        trialIDX = [1:41 NaN 42:57 NaN 58:59 61:68 70:112 114:149 151 NaN 152:187 ...
            189:239 241:249 251:260 262:310 312:320 322:355 NaN 356:360 NaN ...
            361:366 NaN 367:378];
        missingIDX = [60 69 113 150 188 240 250 261 311 321];
        extraIDX = [42 58 152 356 361 367];
    elseif sbj == 15
        trialIDX = [1:6 NaN 7:95 97:124 126:155 NaN 156:162 164:165 NaN 166:172 ...
            174:217 219:252 NaN 253:324 326:353 355:372 NaN 373:378];
        missingIDX = [96 125 163 173 218 325 354];
        extraIDX = [7 156 166 253 373];
    elseif sbj == 16
        trialIDX = [1:19 21:29 31:49 NaN 50:132 134:153 155:174 176:190 NaN ...
            191:232 NaN 233:260 262:293 295:305 308:318 NaN 319:345 347:354 356:378];
        missingIDX = [20 30 133 154 175 261 294 306 307 346 355];
        extraIDX = [50 191 233 319];
    elseif sbj == 17
        trialIDX = [1:35 NaN 36:50 52:66 68:148 NaN 151:159 NaN 162:183 185:213 215:224 ...
            NaN 225:264 266:287 289:299 301:303 NaN 304:333 NaN 336:348 NaN 351:360 ...
            362:378];
        missingIDX = [51 67 149 160 184 214 265 288 300 334 ...
            349 361];
        extraIDX = [36 225 304];
    elseif sbj == 18
        trialIDX = [1:59 61:124 126:147 149:169 171:179 181:197 199:218 NaN NaN 222:232 ...
            234:258 NaN 259:260 262:303 305:348 350:376 NaN NaN];
        missingIDX = [60 125 148 170 180 198 219 220 221 233 261 304 349];
        extraIDX = [259];
    elseif sbj == 19
        trialIDX = [1:3 5:14 16:25 27:50 52:62 64:73 NaN 74:78 80:108 NaN 109:140 NaN 141:153 ...
            155:166 NaN 169:177 179:189 191:240 NaN 243:289 291:302 304:329 ...
            NaN 330:343 NaN 344:347 349:358 NaN 359:361 363:375 377:378];
        missingIDX = [4 15 26 51 63 79 154 168 178 190 242 290 303 348 ...
            362 376];
        extraIDX = [74 109 141 330 344 359];
    elseif sbj == 20
        trialIDX = [1:34 NaN 35:49 51:77 NaN 78:80 82:110 NaN 111:112 114:118 ...
            NaN 119:142 144:154 156:166 NaN 169:177 NaN 178:184 NaN ...
            185:202 204:215 217:240 NaN 243:273 NaN 274:295 NaN 296:338 NaN ...
            341:352 354:378];
        missingIDX = [50 81 113 143 155 168 203 216 239 340 353];
        extraIDX = [35 78 111 119 178 185 274 296];
    elseif sbj == 21
        trialIDX = [1 3:68 70:81 83:106 108:163 165:175 177:187 190:224 226:251 ...
            253:261 NaN 264:287 289:300 302:314 316 318:329 331:341 NaN 342:343 ...
            345:348 NaN 349:371 373:378];
        missingIDX = [2 69 82 107 164 176 188 189 225 252 262 288 301 ...
            315 317 330 344 372];
        extraIDX = [342 349];
    elseif sbj == 22
        trialIDX = [1:9 NaN 12:17 NaN 18:19 21:42 44:54 56:76 NaN 77:88 90:98 ...
            100:104 NaN 105:135 137:169 171:181 183:188 NaN 189:191 193:201 203:212 ...
            214:228 NaN 229:256 NaN 259:302 304:314 316:324 NaN 327:328 NaN 329:337 ...
            339:341 NaN 342:348 350:378];
        missingIDX = [11 20 43 55 89 99 136 170 182 192 202 213 258 303 ...
            315 326 338 349];
        extraIDX = [18 77 105 189 229 329 342];
    elseif sbj == 23
        trialIDX = [1:52 NaN 55:61 NaN 62:119 122:134 NaN 135:141 ... %NaN NaN ... NaN NaN ...
            NaN 145:166 NaN 169:175 NaN 176:196 NaN 197:229 231:253 255:258 NaN ...
            259:263 265:273 NaN 274:287 NaN 288:299 301:323 325:343 NaN 344:350 ...
            NaN 353:378];
        missingIDX = [54 120 121 143 144 168 230 254 264 300 324 352];
        extraIDX = [62 135 176 197 259 274 288 344];
    elseif sbj == 24
        trialIDX = [1:4 6:14 16:29 NaN 30:118 NaN 119:135 138:148 NaN 151:162 ...
            164:187 190:196 198:202 NaN 203:236 238:273 275:313 315:341 343:371 ...
            NaN 372:378];
        missingIDX = [5 15 163 197 237 274 314 342];
        extraIDX = [30 119 203 372];
    elseif sbj == 25
        trialIDX = [1:13 15:24 26:34 NaN NaN 38:57 59:115 117:138 140:143 NaN 144:161 ...
            163:171 173:202 204:228 NaN 229:245 247:248 NaN 249:258 260:264 NaN ...
            265:291 293:302 304:322 324:333 NaN 336:378];
        missingIDX = [14 25 58 116 139 162 172 203 246 259 292 303 323];
        extraIDX = [144 229 249 265];
    elseif sbj == 26
        trialIDX = [1:71 NaN 72:82 84:106 108:111 113:129 131:143 145:196 198:238 ...
            240:244 NaN 245:260 263:274 276:302 304:345 NaN 348:375 NaN NaN NaN];
        missingIDX = [83 107 112 130 144 197 239 261 262 275 303];
        extraIDX = [72 245];
    elseif sbj ==27
        trialIDX = [1:3 NaN 4:37 39:51 NaN 52:112 NaN 113:120 NaN 121:136 138:173 ...
            176:241 NaN 242:255 257:286 NaN 287:290 292:324 NaN 327 NaN 328:378];
        missingIDX = [38 137 138 256 291];
        extraIDX = [4 52 113 121 242 287 328];
    elseif sbj == 28
        trialIDX = [1:12 14:58 60:71 NaN 72 NaN 73:79 81:90 92:110 NaN 111:122 NaN ...
            123:132 134:135 137:158 NaN 159:161 NaN NaN 162:168 170:184 NaN NaN 188:230 ...
            NaN 231:235 237:246 248:268 270:331 333:369 372:378];
        missingIDX = [13 59 80 91 133 136 162 163 169 236 247 269 332];
        extraIDX = [72 73 111 123 159 231];
    elseif sbj == 29
        trialIDX = [1:2 4:64 66:78 NaN 79:87 NaN 88:97 99:117 120:132 134:138 NaN ...
            139:154 156:195 198:218 NaN NaN 222:226 228:232 234:244 246:275 ...
            277:292 NaN 293:338 340:364 366:376 NaN]; % NaN];
        missingIDX = [3 65 98 118 119 133 155 196 197 227 233 245 276 339 365];
        extraIDX = [79 88 139 293];
    elseif sbj == 30
        trialIDX = [1:26 NaN 27:87 NaN 88:123 NaN 124:135 137:174 176:184 186:198 ...
            200:237 239:284 286:305 NaN 306:333 335:354 NaN 355:362 364:378];
        missingIDX = [136 175 185 199 238 285 334 363];
        extraIDX = [27 88 124 306 355];
    elseif sbj == 31
        trialIDX = [1:130 132:158 160:178 NaN 179:222 224:248 NaN 249:255 NaN ...
            256:260 263:287 289:326 329:341 343:355 NaN 358:362 NaN 365:369 ...
            NaN 370:378];
        missingIDX = [131 159 223 261 262 288 327 328 342];
        extraIDX = [179 249 256 370];
    elseif sbj == 32
        trialIDX = [1:4 NaN 5:51 53:109 111:118 NaN 119:130 NaN 131:177 179:194 ...
            NaN 195:199 201:224 226:247 NaN 248:250 252:292 NaN 293:337 339:376 NaN];
        missingIDX = [52 110 178 200 225 251 338];
        extraIDX = [5 119 131 195 248 293];
    elseif sbj == 33
        trialIDX = [1:11 NaN 12:79 81:138 NaN 139:148 151:163 165:266 268:291 ...
            293:331 333:378];
        missingIDX = [80 149 150 164 267 292 332];
        extraIDX = [12 139];
    elseif sbj == 35
        trialIDX = [1:8 10:22 24:70 72:106 108:120 122:158 NaN 159:161 163:173 ...
            175:198 200:235 NaN 236:262 NaN 263:309 311:315 NaN 316:346 NaN ...
            349:374 376:378];
        missingIDX = [9 23 71 107 121 162 174 199 310 375];
        extraIDX = [159 236 263 316];
    elseif sbj == 36
        trialIDX = [1:12 NaN 13:14 16:25 27:86 NaN 87:92 94:123 NaN 124:153 155:176 NaN 179:208 ...
            NaN 209:248 NaN 251:266 NaN 267:280 NaN 283:291 293:301 NaN 302:304 ...
            306:315 317:336 NaN 337:342 344:378];
        missingIDX = [15 26 93 154 292 305 316 343];
        extraIDX = [13 87 124 209 267 302 337];
    elseif sbj == 37
        trialIDX = [1:64 66:110 112:118 NaN 119:129 NaN 132:138 NaN 139:178 180:201 ...
            203:242 NaN 243:252 254:315 317:328 330:353 NaN 354 356:378];
        missingIDX = [];
        extraIDX = [];
    elseif sbj == 38
        trialIDX = [1:12 NaN 13:16 18:39 41:85 88:97 99:109 112:147 149:174 176:189 ...
            192:215 217:241 NaN 242:324 NaN 327:338 NaN 341:354 356:357 359:374 376:378];
        missingIDX = [17 40 86 87 98 110 111 148 175 190 191 216 355 358 375];
        extraIDX = [13 242];
    end
    
%     % sanity check: gdiff must be equal to 0
%     tIDX = trialIDX;
%     g  = find(isnan(trialIDX));
%     tIDX(g) = 1;
%     gdiff = length(digFromTrig) - length(tIDX);
%     if gdiff > 0
%         E = [[digID(tIDX) ; NaN([gdiff 1])] digFromTrig ];
%     else
%         E = [digID(tIDX) [digFromTrig ; NaN([abs(gdiff) 1])]];
%     end
        
    
    

    %% add behavioural info to trials
    DEGRAD_3_LVL = NaN([378 1]);
    tab = readtable([behavDir 'DiNdataClean.csv'],'ReadVariableNames',0);
    
    deg3lvl = str2double(table2array(tab(:,5)));
    idx_block = str2double(table2array(tab(:,2)));
    idx_trialBlock = str2double(table2array(tab(:,3)));
    
    deg3lvl = deg3lvl(2:end);
    idx_block = idx_block(2:end);
    idx_trialBlock = idx_trialBlock(2:end);
    
    for i = 1:length(deg3lvl)
        trialIDdeg(i) = idx_trialBlock(i) + ((idx_block(i) -1) * 63);
    end
    
    for i = 1:length(deg3lvl)
        DEGRAD_3_LVL(trialIDdeg(i)) = deg3lvl(i);
    end
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % make vectors with responses to be added to the event structure
    j = 0;
    
    validTrialIDX = find(~isnan(validTrial));
    TRIAL_IDX = NaN([1 length(EEG.urevent)]);
    DIGIT = NaN([1 length(EEG.urevent)]);
    SONSET = NaN([1 length(EEG.urevent)]);
    DEGLVL = NaN([1 length(EEG.urevent)]);
    DEGBIN = NaN([1 length(EEG.urevent)]);
    ACCUR = NaN([1 length(EEG.urevent)]);
    CLARITY = NaN([1 length(EEG.urevent)]);
    CLARITY_BIN = NaN([1 length(EEG.urevent)]);
    
    validResponseIDX = find(~isnan(validResponse));
    RESPONSE_IDX = NaN([1 length(EEG.urevent)]);
    R_DIGIT = NaN([1 length(EEG.urevent)]);
    R_SONSET = NaN([1 length(EEG.urevent)]);
    R_DEGLVL = NaN([1 length(EEG.urevent)]);
    R_DEGBIN = NaN([1 length(EEG.urevent)]);
    R_ACCUR = NaN([1 length(EEG.urevent)]);
    R_CLARITY = NaN([1 length(EEG.urevent)]);
    R_CLARITY_BIN = NaN([1 length(EEG.urevent)]);
    for i = 1:length(EEG.urevent)
        if ismember(i,validTrialIDX)
            j = j + 1;
            TRIAL_IDX(i) = trialIDX(j);
            if ~isnan(trialIDX(j))
                DIGIT(i) = DIGIT_ID(trialIDX(j));
                SONSET(i) = ITI(trialIDX(j));
                DEGLVL(i) = DEGRAD_LVL_ORIG(trialIDX(j));
                DEGBIN(i) = DEGRAD_3_LVL(trialIDX(j));
                ACCUR(i) = ACCURACY(trialIDX(j));
                CLARITY(i) = CLARITY_ORIG(trialIDX(j));
                CLARITY_BIN(i) = CLARITY3lvls(trialIDX(j));
            end
        end
    end
    
    % MARK RESPONSES WITH APPROPRIATE TRIGGERS
    % IF DUPLICATE TRIGGER, SKIP
    
    id = find(~isnan(TRIAL_IDX));
    R_I = NaN([1 length(id)]);
    for i = 1:length(id)-1 %epStart:epEnd
        nextEvents = {EEG.urevent(id(i)+1:id(i+1)).type};
        %         disp(nextEvents{1})
        if sum(contains(nextEvents,'DI24')) > 0 %isnan(digFromTrig_II(i + 1))
            r_id = find(contains(nextEvents,'DI24'));
            R_I(i) = id(i) + r_id(1);
            %             disp(num2str(R_I(i)))
        end
    end
    i = length(id);
    nextEvents = {EEG.urevent(id(i)+1:epEnd).type};
    if sum(contains(nextEvents,'DI24')) > 0 %isnan(digFromTrig_II(i + 1))
        r_id = find(contains(nextEvents,'DI24'));
        R_I(i) = id(i) + r_id(1);
    end
    
    
    R = R_I;
    Rna = find(isnan(R_I));
    l = find(Rna == 1);
    if ~isempty(l)
        Rna(l) = [];
    end
    R(Rna) = R(Rna-1) + 1;
    j = 0;
    JS = [];
    for i = 1:length(EEG.urevent) %epStart:epEnd
        if ismember(i, R)
            j = j + 1;
            JS = [JS j];
            if ismember(i, R_I)
                if isnan(trialIDX(j)) % ~isnan(trialIDX(j))
                    j = j+1;
                    if ismember(j, extraIDX)
                        extraIDX=extraIDX+1;
                        RESPONSE_IDX(i) = trialIDX(j);
                        %                         j = j-1;
                        R_DIGIT(i) = DIGIT_ID(trialIDX(j));
                        R_SONSET(i) = ITI(trialIDX(j));
                        R_DEGLVL(i) = DEGRAD_LVL_ORIG(trialIDX(j));
                        R_DEGBIN(i) = DEGRAD_3_LVL(trialIDX(j));
                        R_ACCUR(i) = ACCURACY(trialIDX(j));
                        R_CLARITY(i) = CLARITY_ORIG(trialIDX(j));
                        R_CLARITY_BIN(i) = CLARITY3lvls(trialIDX(j));
                    else
                        RESPONSE_IDX(i) = NaN;
                        R_DIGIT(i) = NaN;
                        R_SONSET(i) = NaN;
                        R_DEGLVL(i) = NaN;
                        R_DEGBIN(i) = NaN;
                        R_ACCUR(i) = NaN;
                        R_CLARITY(i) = NaN;
                        R_CLARITY_BIN(i) = NaN;
                    end
                else
                    RESPONSE_IDX(i) = trialIDX(j);
                    R_DIGIT(i) = DIGIT_ID(trialIDX(j));
                    R_SONSET(i) = ITI(trialIDX(j));
                    R_DEGLVL(i) = DEGRAD_LVL_ORIG(trialIDX(j));
                    R_DEGBIN(i) = DEGRAD_3_LVL(trialIDX(j));
                    R_ACCUR(i) = ACCURACY(trialIDX(j));
                    R_CLARITY(i) = CLARITY_ORIG(trialIDX(j));
                    R_CLARITY_BIN(i) = CLARITY3lvls(trialIDX(j));
                end
            end
        end
    end
    
    
    % put together stim trigger idx with response trigger idx and check
    % that the latter is always subsequent to the former
        G = [(TRIAL_IDX)' (RESPONSE_IDX)'];
        

    if sbj == 5
        h = find(RESPONSE_IDX == 259);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    elseif sbj == 7
        h = find(RESPONSE_IDX == 210);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
        h = find(RESPONSE_IDX == 348);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    elseif sbj == 9
        h = find(RESPONSE_IDX == 43);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
        h = find(RESPONSE_IDX == 169);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    elseif sbj == 10
        h = find(RESPONSE_IDX == 34);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
        RESPONSE_IDX(306) = 42;
        h = find(RESPONSE_IDX == 43);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
        h1 = find(RESPONSE_IDX == 107); h2 = find(RESPONSE_IDX == 108);
        RESPONSE_IDX(h1:h2) = RESPONSE_IDX(h1:h2)+1;
        h1 = find(RESPONSE_IDX == 140); h2 = find(RESPONSE_IDX == 141);
        RESPONSE_IDX(h1:h2) = RESPONSE_IDX(h1:h2)+1;
        h1 = find(RESPONSE_IDX == 198); h2 = find(RESPONSE_IDX == 199);
        RESPONSE_IDX(h1:h2) = RESPONSE_IDX(h1:h2)+1;
        h1 = find(RESPONSE_IDX == 321); h2 = find(RESPONSE_IDX == 324);
        RESPONSE_IDX(h1:h2) = RESPONSE_IDX(h1:h2)+1;
        h1 = find(RESPONSE_IDX == 333); h2 = find(RESPONSE_IDX == 334);
        RESPONSE_IDX(h1)=334; RESPONSE_IDX(h2)=335;
        h1 = find(RESPONSE_IDX == 346); h2 = find(RESPONSE_IDX == 347);
        RESPONSE_IDX(h1)=347; RESPONSE_IDX(h2)=348;
        h1 = find(RESPONSE_IDX == 358); h2 = find(RESPONSE_IDX == 360);
        RESPONSE_IDX(h1:h2) = RESPONSE_IDX(h1:h2)+1;
    elseif sbj == 11
        h = find(RESPONSE_IDX == 27);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+2;
        h1 = find(RESPONSE_IDX == 30); h2 = find(RESPONSE_IDX == 31);
        RESPONSE_IDX(h1:h2) = RESPONSE_IDX(h1:h2)+1;
        h1 = find(RESPONSE_IDX == 42); h2 = find(RESPONSE_IDX == 43);
        RESPONSE_IDX(h1:h2) = RESPONSE_IDX(h1:h2)+1;
        h1 = find(RESPONSE_IDX == 239); h2 = find(RESPONSE_IDX == 240);
        RESPONSE_IDX(h1:h2) = RESPONSE_IDX(h1:h2)+1;
        h1 = find(RESPONSE_IDX == 366); h2 = find(RESPONSE_IDX == 367);
        RESPONSE_IDX(h1:h2) = RESPONSE_IDX(h1:h2)+1;
    elseif sbj == 12
        h = find(RESPONSE_IDX == 226);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
        h = find(RESPONSE_IDX == 293);
        RESPONSE_IDX(h) = 295;
    elseif sbj == 15
        h = find(RESPONSE_IDX == 18);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
        h = find(RESPONSE_IDX == 339);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
        h1 = find(RESPONSE_IDX == 354); h2 = find(RESPONSE_IDX == 355);
        RESPONSE_IDX(h1:h2) = RESPONSE_IDX(h1:h2)+1;
    elseif sbj == 16
        h = find(RESPONSE_IDX == 1);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
        h = find(RESPONSE_IDX == 51);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
        h1 = find(RESPONSE_IDX == 175); h2 = find(RESPONSE_IDX == 176);
        RESPONSE_IDX(h1:h2) = RESPONSE_IDX(h1:h2)+1;
    elseif sbj == 17
        h = find(RESPONSE_IDX == 28);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
        h = find(RESPONSE_IDX == 160);
        RESPONSE_IDX(h) = 162;
        h = find(RESPONSE_IDX == 300);
        RESPONSE_IDX(h) = 301;
        h = find(RESPONSE_IDX == 334);
        RESPONSE_IDX(h) = 336;
        h = find(RESPONSE_IDX == 349);
        RESPONSE_IDX(h) = 351;
        h = find(RESPONSE_IDX == 361);
        RESPONSE_IDX(h) = 362;
    elseif sbj == 18
         h = find(RESPONSE_IDX == 222);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
         h = find(RESPONSE_IDX == 323);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
        h = find(RESPONSE_IDX == 363);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    elseif sbj == 19
        h = find(RESPONSE_IDX == 142);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
        RESPONSE_IDX(629) = 155;
        RESPONSE_IDX(735) = 191;
        RESPONSE_IDX(1016) = 291;
    elseif sbj == 20
        h = find(RESPONSE_IDX == 180);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
        RESPONSE_IDX(774) = 204;
        RESPONSE_IDX(810) = 217;
        RESPONSE_IDX(881) = 243;
        RESPONSE_IDX(1205) = 354;
        h = find(RESPONSE_IDX == 365);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    elseif sbj == 21
        h = find(RESPONSE_IDX == 47);
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
        RESPONSE_IDX(389) = 70;
        RESPONSE_IDX(425) = 83;
        RESPONSE_IDX(493) = 108;
        RESPONSE_IDX(830) = 226;
        RESPONSE_IDX(906) = 253;
        RESPONSE_IDX(935) = 264;
        RESPONSE_IDX(1040) = 302;
        RESPONSE_IDX(1081:1086) = RESPONSE_IDX(1081:1086)+1;
        RESPONSE_IDX(1123) = 331;
        RESPONSE_IDX(1237) = 373;
    elseif sbj == 22
        RESPONSE_IDX(222) = 10;
        RESPONSE_IDX(225) = 11;
        RESPONSE_IDX(228) = 12;
        RESPONSE_IDX(252) = 20;
        RESPONSE_IDX(314) = 43;
        RESPONSE_IDX(346) = 55;
        RESPONSE_IDX(407) = 77;
        RESPONSE_IDX(441) = 89;
        RESPONSE_IDX(469) = 99;
        RESPONSE_IDX(486) = 105;
        RESPONSE_IDX(576) = 136;
        RESPONSE_IDX(706) = 182;
        RESPONSE_IDX(728) = 189;
        RESPONSE_IDX(738) = 192;
        RESPONSE_IDX(765) = 202;
        RESPONSE_IDX(796) = 213;
        RESPONSE_IDX(840) = 229;
        RESPONSE_IDX(898) = 250;
        h = 901;
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
        RESPONSE_IDX(920) = 256;
        RESPONSE_IDX(922) = 257;
        RESPONSE_IDX(924) = 258;
        RESPONSE_IDX(927) = 259;
        RESPONSE_IDX(930) = 260;
        h = 986;
        RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
        RESPONSE_IDX(1046) = 303;
        RESPONSE_IDX(1049) = 304;
        RESPONSE_IDX(1052) = 305;
        RESPONSE_IDX(1084) = 316;
        RESPONSE_IDX(1087) = 317;
        RESPONSE_IDX(1110) = 325;
        RESPONSE_IDX(1113) = 326;
        RESPONSE_IDX(1116) = 327;
        RESPONSE_IDX(1119) = 328;
        RESPONSE_IDX(1123) = 329;
        RESPONSE_IDX(1129) = 331;
        RESPONSE_IDX(1149) = 339;
        RESPONSE_IDX(1152) = 340;
        RESPONSE_IDX(1164) = 344;
        RESPONSE_IDX(1178) = 350;
        RESPONSE_IDX(1181) = 351;
    end
    
% CHECK IF TRIALS WITH MISSING STIMULUS TRIGGER HAVE RESPONSE TRIGGER
% IF SO, ADD
for m = 1:length(missingIDX)
    M = missingIDX(m);
    for i = find(RESPONSE_IDX == M-1)+1:find(RESPONSE_IDX == M+1)-1
        theseEvents = EEG.urevent(i).type;
        if contains(theseEvents,'DI24')
            RESPONSE_IDX(i) = M;
            R_DIGIT(i) = DIGIT_ID(trialIDX(j));
            R_SONSET(i) = ITI(trialIDX(j));
            R_DEGLVL(i) = DEGRAD_LVL_ORIG(trialIDX(j));
            R_DEGBIN(i) = DEGRAD_3_LVL(trialIDX(j));
            R_ACCUR(i) = ACCURACY(trialIDX(j));
            R_CLARITY(i) = CLARITY_ORIG(trialIDX(j));
            R_CLARITY_BIN(i) = CLARITY3lvls(trialIDX(j));
            disp(['added nr ' num2str(M)]);
        end
    end
end

% h = 986;
% RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
% RESPONSE_IDX(1036) = 297;

G = [(TRIAL_IDX)' (RESPONSE_IDX)'];  

if sbj == 4
    RESPONSE_IDX(495) = 105;
    RESPONSE_IDX(628:629) = NaN;
    RESPONSE_IDX(816) = 222;
    RESPONSE_IDX(819) = 223;
    RESPONSE_IDX(822) = 224;
    RESPONSE_IDX(1005) = 289;
    RESPONSE_IDX(1008) = 290;
    RESPONSE_IDX(1011) = 291;
    RESPONSE_IDX(1095) = 319;
elseif sbj == 5
    RESPONSE_IDX(788) = 212;
    RESPONSE_IDX(812) = 220;
    RESPONSE_IDX(1038) = 303;
    RESPONSE_IDX(1063) = 312;
    RESPONSE_IDX(1126) = 332;
    RESPONSE_IDX(1130) = 333;
    RESPONSE_IDX(1139) = 336;
    RESPONSE_IDX(1143) = 337;
    RESPONSE_IDX(1151) = 340;
    RESPONSE_IDX(1174) = 348;
    RESPONSE_IDX(1178) = 349;
    RESPONSE_IDX(1192) = 354;
    RESPONSE_IDX(1260) = 377;
elseif sbj == 6
    RESPONSE_IDX(247) = 19;
    RESPONSE_IDX(248) = 20;
    RESPONSE_IDX(251) = 21;
    RESPONSE_IDX(376) = 65;
    RESPONSE_IDX(436) = 86;
    RESPONSE_IDX(476) = 101;
    RESPONSE_IDX(587) = 140;
    RESPONSE_IDX(1034) = 300;
elseif sbj == 8
    RESPONSE_IDX(1013) = 289;
    RESPONSE_IDX(1016) = 290;
    RESPONSE_IDX(1019) = 291;
    RESPONSE_IDX(1097) = 318;
elseif sbj == 9
    RESPONSE_IDX(1036) = 297;
    RESPONSE_IDX(1039) = 298;
    RESPONSE_IDX(1228) = 364;
    RESPONSE_IDX(1231) = 365;
elseif sbj == 10
    RESPONSE_IDX(296) = 38;
    RESPONSE_IDX(299) = 39;
    RESPONSE_IDX(300) = 40;
    RESPONSE_IDX(303) = 41;
    RESPONSE_IDX(309) = 43;
    RESPONSE_IDX(331) = 51;
    RESPONSE_IDX(406) = 76;
    RESPONSE_IDX(408) = 77;
    RESPONSE_IDX(443) = 89;
    RESPONSE_IDX(587) = 140;
    RESPONSE_IDX(739) = 193;
    RESPONSE_IDX(882) = 244;
    RESPONSE_IDX(1109) = 324;
    RESPONSE_IDX(1247) = 374;
    RESPONSE_IDX(1250) = 375;
elseif sbj == 11
    RESPONSE_IDX(354) = 55;
    RESPONSE_IDX(357) = 56;
    RESPONSE_IDX(437) = 83;
    RESPONSE_IDX(439) = 84;
    RESPONSE_IDX(533) = 119;
    RESPONSE_IDX(536) = 120;
    RESPONSE_IDX(723) = 185;
    RESPONSE_IDX(726) = 186;
    RESPONSE_IDX(1214) = 353;
    RESPONSE_IDX(1216) = 354;
elseif sbj == 12
    RESPONSE_IDX(287) = 32;
    RESPONSE_IDX(578) = 134;
    RESPONSE_IDX(1029) = 293;
    RESPONSE_IDX(1030) = 294;
elseif sbj == 13
    RESPONSE_IDX(213) = 6;
    RESPONSE_IDX(217) = 8;
    RESPONSE_IDX(298) = 37;
    RESPONSE_IDX(472) = 100;
    RESPONSE_IDX(507) = 113;
    RESPONSE_IDX(658) = 166;
    RESPONSE_IDX(660) = 167;
    RESPONSE_IDX(662) = 168;
    RESPONSE_IDX(716) = 188;
    RESPONSE_IDX(818) = 224;
    RESPONSE_IDX(854) = 236;
    RESPONSE_IDX(918) = 258;
    RESPONSE_IDX(949) = 269;
    RESPONSE_IDX(1012) = 292;
    RESPONSE_IDX(1013) = NaN;
    RESPONSE_IDX(1050) = 307;
    RESPONSE_IDX(1257) = 378;
elseif sbj == 14
    RESPONSE_IDX(319) = 42;
    RESPONSE_IDX(364) = 58;
    RESPONSE_IDX(1199) = 356;
    RESPONSE_IDX(1232) = 367;
elseif sbj == 15
    RESPONSE_IDX(1125) = 326;
    RESPONSE_IDX(919) = 254;
    RESPONSE_IDX(683) = 173;
    RESPONSE_IDX(686) = 174;
    RESPONSE_IDX(667) = 167;
    RESPONSE_IDX(656) = 163;
    RESPONSE_IDX(659) = 164;
    RESPONSE_IDX(551) = 126;
    RESPONSE_IDX(479) = 97;
    RESPONSE_IDX(227) = 7;
elseif sbj == 16
    RESPONSE_IDX(562) = 134;
    RESPONSE_IDX(565) = 135;
    RESPONSE_IDX(619) = 155;
    RESPONSE_IDX(622) = 156;
    RESPONSE_IDX(1058) = 308;
    RESPONSE_IDX(1060) = 309;
    RESPONSE_IDX(1173) = 347;
    RESPONSE_IDX(1176) = 348;
    RESPONSE_IDX(1195) = 356;
    RESPONSE_IDX(1198) = 357;
    RESPONSE_IDX(274) = 30;
    RESPONSE_IDX(277) = 31;
    RESPONSE_IDX(734) = 193;
elseif sbj == 17
    RESPONSE_IDX(1182) = 349;
    RESPONSE_IDX(1185) = 350;
    RESPONSE_IDX(1149) = 337;
    RESPONSE_IDX(1143) = 334;
    RESPONSE_IDX(1145) = 335;
    RESPONSE_IDX(1058) = 305;
    RESPONSE_IDX(1042) = 300;
    RESPONSE_IDX(651) = 163;
    RESPONSE_IDX(643) = 160;
    RESPONSE_IDX(645) = 161;
    RESPONSE_IDX(613) = 149;
    RESPONSE_IDX(616) = 150;
    RESPONSE_IDX(618) = 151;
    RESPONSE_IDX(620) = 152;
    RESPONSE_IDX(380) = 67;
    RESPONSE_IDX(382) = 68;
    RESPONSE_IDX(337) = 51;
    RESPONSE_IDX(339) = 52;
    RESPONSE_IDX(301) = 37;
elseif sbj == 18
    h = find(RESPONSE_IDX == 222);
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    h = find(RESPONSE_IDX == 323);
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    h = find(RESPONSE_IDX == 363);
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    h = find(RESPONSE_IDX == 233);
    RESPONSE_IDX(h) = RESPONSE_IDX(h)+1;
    h = find(RESPONSE_IDX == 234);
    RESPONSE_IDX(h) = RESPONSE_IDX(h)+1;
    h = find(RESPONSE_IDX == 261);
    RESPONSE_IDX(h) = RESPONSE_IDX(h)+1;
    RESPONSE_IDX(1260) = 377;
    RESPONSE_IDX(1264) = 378;
    RESPONSE_IDX(936) = 260;
    RESPONSE_IDX(938) = 261;
    RESPONSE_IDX(819) = 219;
    RESPONSE_IDX(820) = 220;
    RESPONSE_IDX(823) = 221;
    RESPONSE_IDX(826) = 222;
elseif sbj == 19
    RESPONSE_IDX(880) = 243;
    RESPONSE_IDX(1256) = 377;
    RESPONSE_IDX(238) = 15;
    RESPONSE_IDX(398) = 74;
    RESPONSE_IDX(497) = 109;
    RESPONSE_IDX(593) = 142;
    RESPONSE_IDX(696) = 178;
    RESPONSE_IDX(699) = 179;
    RESPONSE_IDX(883) = 244;
    RESPONSE_IDX(874) = 241;
    RESPONSE_IDX(877) = 242;
    RESPONSE_IDX(1134) = 331;
    RESPONSE_IDX(1220) = 363;
elseif sbj == 20
    RESPONSE_IDX(1169) = 341;
    RESPONSE_IDX(296) = 35;
    RESPONSE_IDX(666) = 167;
    RESPONSE_IDX(667) = 168;
    RESPONSE_IDX(670) = 169;
    RESPONSE_IDX(698) = 178;
    RESPONSE_IDX(875) = 241;
    RESPONSE_IDX(878) = 242;
    RESPONSE_IDX(884) = 244;
    RESPONSE_IDX(977) = 275;
    RESPONSE_IDX(1042) = 297;
    RESPONSE_IDX(1164) = 339;
    RESPONSE_IDX(1167) = 340;
    RESPONSE_IDX(1172) = 342;
elseif sbj == 21
    RESPONSE_IDX(657) = 165;
    RESPONSE_IDX(691) = 177;
    RESPONSE_IDX(654) = 164;
    RESPONSE_IDX(689) = 176;
    RESPONSE_IDX(722) = 188;
    RESPONSE_IDX(724) = 189;
    RESPONSE_IDX(729) = 190;
    RESPONSE_IDX(937) = 265;
    RESPONSE_IDX(1000) = 288;
    RESPONSE_IDX(1003) = 289;
    RESPONSE_IDX(1037) = 301;
    RESPONSE_IDX(1157) = 343;
    RESPONSE_IDX(1176) = 350;
elseif sbj == 22
    RESPONSE_IDX(1079) = 315;
    RESPONSE_IDX(920:924) = NaN;
    RESPONSE_IDX(895) = 249;
elseif sbj == 23
    RESPONSE_IDX(533) = 221;
    RESPONSE_IDX(573) = 135;
    RESPONSE_IDX(593) = 142;
    RESPONSE_IDX(595) = 143;
    RESPONSE_IDX(597) = 144;
    RESPONSE_IDX(600) = 145;
    RESPONSE_IDX(663) = 167;
    RESPONSE_IDX(664) = 168;
    RESPONSE_IDX(667) = 169;
    RESPONSE_IDX(689) = 176;
    RESPONSE_IDX(753) = 197;
    RESPONSE_IDX(929) = 259;
    RESPONSE_IDX(970) = 274;
    RESPONSE_IDX(1011) = 288;
    RESPONSE_IDX(1045) = 300;
    RESPONSE_IDX(1173) = 344;
    RESPONSE_IDX(1190) = 351;
    RESPONSE_IDX(1192) = 352;
    RESPONSE_IDX(1194) = 353;
elseif sbj == 24
    RESPONSE_IDX(282) = 30;
    RESPONSE_IDX(584) = 136;
    RESPONSE_IDX(585) = 137;
    RESPONSE_IDX(621) = 150;
    RESPONSE_IDX(623) = 151;
    RESPONSE_IDX(729) = 188;
    RESPONSE_IDX(730) = 189;
    RESPONSE_IDX(771) = 203;
    RESPONSE_IDX(862) = 237;
    RESPONSE_IDX(1252) = 372;
elseif sbj == 25
    RESPONSE_IDX(96) = 35;
    RESPONSE_IDX(99) = 36;
    RESPONSE_IDX(102) = 37;
    RESPONSE_IDX(105) = 38;
    h = 108;
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    %         RESPONSE_IDX(359) = 129;
    RESPONSE_IDX(404) = 145;
    RESPONSE_IDX(479) = 172;
    RESPONSE_IDX(482) = 173;
    RESPONSE_IDX(570) = 203;
    RESPONSE_IDX(573) = 204;
    RESPONSE_IDX(645) = 230;
    RESPONSE_IDX(690) = 246;
    RESPONSE_IDX(693) = 247;
    RESPONSE_IDX(703) = 250;
    RESPONSE_IDX(732) = 259;
    RESPONSE_IDX(735) = 260;
    RESPONSE_IDX(751) = 266;
    RESPONSE_IDX(823) = 292;
    RESPONSE_IDX(826) = 293;
    RESPONSE_IDX(855) = 303;
    RESPONSE_IDX(858) = 304;
    RESPONSE_IDX(917) = 324;
    RESPONSE_IDX(947) = 334;
    RESPONSE_IDX(949) = 335;
    RESPONSE_IDX(951) = 336;
    RESPONSE_IDX(953) = 337;
elseif sbj == 26
    RESPONSE_IDX(393) = 72;
    RESPONSE_IDX(882) = 245;
    RESPONSE_IDX(1172) = 346;
    RESPONSE_IDX(1175) = 347;
    RESPONSE_IDX(1178) = 348;
    RESPONSE_IDX(1255) = 376;
    RESPONSE_IDX(1257) = 377;
    RESPONSE_IDX(1259) = 378;
elseif sbj == 27
    RESPONSE_IDX(346) = 52;
    h = 372;
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    RESPONSE_IDX(515) = 114;
    RESPONSE_IDX(538) = 122;
    RESPONSE_IDX(584) = 138;
    RESPONSE_IDX(684) = 174;
    RESPONSE_IDX(686) = 175;
    RESPONSE_IDX(689) = 176;
    RESPONSE_IDX(881) = 243;
    RESPONSE_IDX(1012) = 288;
    RESPONSE_IDX(1121) = 325;
    RESPONSE_IDX(1122) = 326;
    RESPONSE_IDX(1125) = 327;
    RESPONSE_IDX(1129) = 328;
elseif sbj == 28
    RESPONSE_IDX(396) = 72;
    RESPONSE_IDX(507) = 111;
    RESPONSE_IDX(541) = 123;
    RESPONSE_IDX(643) = 159;
    h1 = 647; h2=654;
    RESPONSE_IDX(h1:h2) = RESPONSE_IDX(h1:h2) - 1;
    h = 660;
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end) + 1;
    RESPONSE_IDX(672) = 169;
    RESPONSE_IDX(675) = 170;
    RESPONSE_IDX(720) = 185;
    RESPONSE_IDX(722) = 186;
    RESPONSE_IDX(725) = 187;
    RESPONSE_IDX(728) = 188;
    RESPONSE_IDX(731) = 189;
    h = 736;
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end) + 1;
    RESPONSE_IDX(857) = 233;
    RESPONSE_IDX(865) = 236;
    h1 = 868; h2=870;
    RESPONSE_IDX(h1:h2) = RESPONSE_IDX(h1:h2) + 1;
    RESPONSE_IDX(896) = 247;
    h1 = 899; h2=902;
    RESPONSE_IDX(h1:h2) = RESPONSE_IDX(h1:h2) + 1;
    RESPONSE_IDX(959) = 269;
    h1 = 962; h2=965;
    RESPONSE_IDX(h1:h2) = RESPONSE_IDX(h1:h2) + 1;
    h1 = 1142; h2=1145;
    RESPONSE_IDX(h1:h2) = RESPONSE_IDX(h1:h2) + 1;
elseif sbj == 29
    RESPONSE_IDX(525) = 118;
    RESPONSE_IDX(527) = 119;
    RESPONSE_IDX(528) = 120;
    RESPONSE_IDX(578) = 137;
    RESPONSE_IDX(581) = 138;
    RESPONSE_IDX(584) = 139;
    RESPONSE_IDX(749) = 196;
    RESPONSE_IDX(751) = 197;
    %     RESPONSE_IDX(814) = 219;
    %     RESPONSE_IDX(817) = 220;
    RESPONSE_IDX(820) = 222;
    h = 823;
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    RESPONSE_IDX(835) = 228;
    RESPONSE_IDX(882) = 245;
    RESPONSE_IDX(885) = 246;
    RESPONSE_IDX(972) = 277;
    RESPONSE_IDX(1021) = 294;
    RESPONSE_IDX(1152) = 339;
    RESPONSE_IDX(1155) = 340;
    RESPONSE_IDX(1222) = 365;
    RESPONSE_IDX(1225) = 366;
elseif sbj == 30
    RESPONSE_IDX(449) = 88;
    RESPONSE_IDX(552) = 124;
    RESPONSE_IDX(625) = 150;
    h = 627;
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    RESPONSE_IDX(761) = 199;
    RESPONSE_IDX(764) = 200;
    h = 1044;
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    RESPONSE_IDX(1069) = 308;
    RESPONSE_IDX(1210) = 357;
    RESPONSE_IDX(1226) = 363;
    RESPONSE_IDX(1228) = 364;
    RESPONSE_IDX(1232) = 365;
elseif sbj == 31
    RESPONSE_IDX(699) = 179;
    RESPONSE_IDX(899) = 249;
    RESPONSE_IDX(1125) = 327;
    RESPONSE_IDX(1203) = 356;
    RESPONSE_IDX(1206) = 357;
    RESPONSE_IDX(1209) = 358;
    RESPONSE_IDX(1223) = 363;
    RESPONSE_IDX(1225) = 364;
    RESPONSE_IDX(1228) = 365;
    RESPONSE_IDX(1241) = 370;
elseif sbj == 32
    RESPONSE_IDX(15) = 5;
    h = 46;
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    RESPONSE_IDX(146) = 52;
    RESPONSE_IDX(149) = 53;
    RESPONSE_IDX(709) = 249;
    RESPONSE_IDX(962) = 338;
    RESPONSE_IDX(965) = 339;
    RESPONSE_IDX(1068) = 377;
    RESPONSE_IDX(1071) = 378;
elseif sbj == 33
    h = 317;
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    h = 484;
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    h = 578;
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    RESPONSE_IDX(592) = 142;
    h = 613;
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+2;
    RESPONSE_IDX(613) = 149;
    RESPONSE_IDX(615) = 150;
    RESPONSE_IDX(616) = 151;
    h = 624;
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)-2;
    h = 652;
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    RESPONSE_IDX(h) = 163;
    h = 663;
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)-1;
    RESPONSE_IDX(945) = 267;
    h = 948;
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    RESPONSE_IDX(957:974) = RESPONSE_IDX(957:974)-1;
    RESPONSE_IDX(1012:1027) = RESPONSE_IDX(1012:1027)+1;
    RESPONSE_IDX(1133:1145) = RESPONSE_IDX(1133:1145)+1;
elseif sbj == 35
    RESPONSE_IDX(640) = 159;
    RESPONSE_IDX(855) = 236;
    RESPONSE_IDX(938) = 263;
    RESPONSE_IDX(1178) = 347;
    RESPONSE_IDX(1180) = 348;
    RESPONSE_IDX(1182) = 349;
elseif sbj == 36
    RESPONSE_IDX(233) = 13;
    h = 553;
    RESPONSE_IDX(h:end) = RESPONSE_IDX(h:end)+1;
    RESPONSE_IDX(699) = 179;
    RESPONSE_IDX(702) = 180;
    RESPONSE_IDX(794) = 210;
    RESPONSE_IDX(900) = 249;
    RESPONSE_IDX(903) = 250;
    RESPONSE_IDX(906) = 251;
    RESPONSE_IDX(909) = 252;
    RESPONSE_IDX(957) = 268;
    RESPONSE_IDX(995) = 282;
    RESPONSE_IDX(997) = 283;
    RESPONSE_IDX(1000) = 284;
    RESPONSE_IDX(1025) = 293;
    RESPONSE_IDX(1056) = 303;
    RESPONSE_IDX(1094) = 317;
    RESPONSE_IDX(1155) = 338;
    RESPONSE_IDX(1167) = 343;
    RESPONSE_IDX(1170) = 344;
elseif sbj == 37
    RESPONSE_IDX(374) = 65;
    RESPONSE_IDX(557) = 130;
    RESPONSE_IDX(560) = 131;
    RESPONSE_IDX(563) = 132;
    RESPONSE_IDX(584) = 139;
    RESPONSE_IDX(761) = 202;
    RESPONSE_IDX(875) = 243;
    RESPONSE_IDX(904) = 253;
    RESPONSE_IDX(1120) = 329;
    RESPONSE_IDX(1192) = 355;
elseif sbj == 38
    RESPONSE_IDX(228) = 13;
    RESPONSE_IDX(428) = 86;
    RESPONSE_IDX(429) = 87;
    RESPONSE_IDX(857) = 242;
    RESPONSE_IDX(1100) = 325;
    RESPONSE_IDX(1102) = 326;
    RESPONSE_IDX(1105) = 327;
    RESPONSE_IDX(1140) = 340;
    RESPONSE_IDX(1142) = 341;
end

 G = [(TRIAL_IDX)' (RESPONSE_IDX)'];

% ADD TRIAL IDX AND BEHAVIOURAL INFO TO EEGLAB EPOCH AND EVENT STRUCTURES
%     T0 = num2cell(TRIAL_IDX);
%     [EEG.urevent.trialIDX] = T0{:};
%     T1 = num2cell(RESPONSE_IDX);
%     [EEG.urevent.responseIDX] = T1{:};
%     T2 = num2cell(DIGIT);
%     [EEG.urevent.digitID] = deal(T2{:});
%     T3 = num2cell(SONSET);
%     [EEG.urevent.ITI] = deal(T3{:});
%     T4 = num2cell(DEGLVL);
%     [EEG.urevent.degLvlOrig] = deal(T4{:});
%     T5 = num2cell(DEGBIN);
%     [EEG.urevent.degBin] = deal(T5{:});
%     T6 = num2cell(ACCUR);
%     [EEG.urevent.accuracy] = deal(T6{:});
%     T7 = num2cell(CLARITY);
%     [EEG.urevent.clarityOrig] = deal(T7{:});
%      T8 = num2cell(CLARITY_BIN);
%     [EEG.urevent.clarityBin] = deal(T8{:});
%     T9 = num2cell(R_DIGIT);
%     [EEG.urevent.R_digitID] = deal(T9{:});
%     T10 = num2cell(R_SONSET);
%     [EEG.urevent.R_ITI] = deal(T10{:});
%     T11 = num2cell(R_DEGLVL);
%     [EEG.urevent.R_degLvlOrig] = deal(T11{:});
%     T12 = num2cell(R_DEGBIN);
%     [EEG.urevent.R_degBin] = deal(T12{:});
%     T13 = num2cell(R_ACCUR);
%     [EEG.urevent.R_accuracy] = deal(T13{:});
%     T14 = num2cell(R_CLARITY);
%     [EEG.urevent.R_clarityOrig] = deal(T14{:});
%     T15 = num2cell(R_CLARITY_BIN);
%     [EEG.urevent.R_clarityBin] = deal(T15{:});
%     
%     pop_saveset(EEG,'filename',[EEG.setname(1:end-4) '_wTrialInfo.set'],...
%         'filepath',outDir)
%     
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    % EPOCH
    EEG = pop_epoch(EEG, {'DI24'}, [-4.3  1], 'newname', ... % [-7  1]
        ['sbj_' num2str(sbj) '_DiN_downsamp_filt_wTrialInfo_epoched.set'], 'epochinfo', 'yes');
    EEG = eeg_checkset(EEG);
    [ALLEEG EEG CURRENTSET] = eeg_store(ALLEEG, EEG, CURRENTSET);
    eeglab redraw
    pop_saveset(EEG,'filename',EEG.setname,'filepath',outDir)
    
    
    X = {EEG.epoch.eventtype};
    Y = {EEG.epoch.eventurevent};
    Z = NaN([1 length(X)]);
    for i = 1:length(X)
        j = cell2mat(Y{i});
        Xid = find(contains(X{i},'DI24'));
        if length(Xid) == 2
            if ismember(Z(i-1),j)
                Xid = Xid(2);
            elseif sum(ismember(j,cell2mat(Y{i+1}))) > 0
                Xid = Xid(1);
            else
                Xid = Xid(1);
            end
        end     
        Z(i) = j(Xid);
    end
    
    RZ = RESPONSE_IDX(Z);
    NR = find(isnan(RZ));
    if sbj == 18 || sbj == 29
        for i = 1:368
            if ismember(i, NR)
                if (RZ(i-1)) == ((RZ(i+1)) - 2)
                    RZ(i) = (RZ(i-1)) + 1;
                    %                 disp(num2str(i))
                end
            end
        end
    else
        for i = 1:length(RZ)
            if ismember(i, NR)
                if (RZ(i-1)) == ((RZ(i+1)) - 2)
                    RZ(i) = (RZ(i-1)) + 1;
                    %                 disp(num2str(i))
                end
            end
        end
    end
    
%     U = cell2mat({EEG.event.urevent});
%     
%     TR = RESPONSE_IDX(U);
%     DI = R_DIGIT(U);
%     IT = R_SONSET(U);
%     DL = R_DEGLVL(U);
%     DB = R_DEGBIN(U);
%     AC = R_ACCUR(U);
%     CL = R_CLARITY(U);
%     CB = R_CLARITY_BIN(U);
    
    TR = RESPONSE_IDX(Z);
%     DI = R_DIGIT(Z);
%     IT = R_SONSET(Z);
%     DL = R_DEGLVL(Z);
%     DB = R_DEGBIN(Z);
%     AC = R_ACCUR(Z);
%     CL = R_CLARITY(Z);
%     CB = R_CLARITY_BIN(Z);

%     R0 = num2cell(TR);
%     [EEG.event.trialIDX] = deal(R0{:});
%     R1 = num2cell(DI);
%     [EEG.event.digitID] = deal(R1{:});
%     R2 = num2cell(IT);
%     [EEG.event.ITI] = deal(R2{:});
%     R3 = num2cell(DL);
%     [EEG.event.degLvlOrig] = deal(R3{:});
%     R4 = num2cell(DB);
%     [EEG.event.degBin] = deal(R4{:});
%     R5 = num2cell(AC);
%     [EEG.event.accuracy] = deal(R5{:});
%     R6 = num2cell(CL);
%     [EEG.event.clarityOrig] = deal(R6{:});
%     R7 = num2cell(CB);
%     [EEG.event.clarityBin] = deal(R7{:});
    

    epTR = NaN([1 length(EEG.epoch)]);
%     epDI = NaN([1 length(EEG.epoch)]);
%     epIT = NaN([1 length(EEG.epoch)]);
%     epDL = NaN([1 length(EEG.epoch)]);
%     epDB = NaN([1 length(EEG.epoch)]);
%     epAC = NaN([1 length(EEG.epoch)]);
%     epCL = NaN([1 length(EEG.epoch)]);
%     epCB = NaN([1 length(EEG.epoch)]);
    
    for i = 1:length(EEG.epoch)
        if ~isnan(RZ(i))
            epTR(i) = RZ(i);
%             epDI(i) = DI(i);
%             epIT(i) = IT(i);
%             epDL(i) = DL(i);
%             epDB(i) = DB(i);
%             epAC(i) = AC(i);
%             epCL(i) = CL(i);
%             epCB(i) = CB(i);
        end
    end
    
%     epochEvent = {EEG.epoch.event};
%     eventEpoch = cell2mat({EEG.event.epoch});
%     un = unique(eventEpoch);
%     for i = 1:length(un)
%         y = find(eventEpoch == i);
%         tIDX = find(~isnan(TR(y)));
%         if ~isempty(tIDX)
%             %         if isempty(tIDX) || length(tIDX) > 1
%             %            tIDX = 1;
%             %         end
%             y = y(tIDX);
%             epTR(i) = TR(y);
%             epDI(i) = DI(y);
%             epIT(i) = IT(y);
%             epDL(i) = DL(y);
%             epDB(i) = DB(y);
%             epAC(i) = AC(y);
%             epCL(i) = CL(y);
%             epCB(i) = CB(y);
%         else
%             epTR(i) = NaN;
%             epDI(i) = NaN;
%             epIT(i) = NaN;
%             epDL(i) = NaN;
%             epDB(i) = NaN;
%             epAC(i) = NaN;
%             epCL(i) = NaN;
%             epCB(i) = NaN;
%         end
%     end
    
    E0 = num2cell(epTR);
    [EEG.epoch.trialIDX] = deal(E0{:});
%     E1 = num2cell(epDI);
%     [EEG.epoch.digitID] = deal(E1{:});
%     E2 = num2cell(epIT);
%     [EEG.epoch.ITI] = deal(E2{:});
%     E3 = num2cell(epDL);
%     [EEG.epoch.degLvlOrig] = deal(E3{:});
%     E4 = num2cell(epDB);
%     [EEG.epoch.degBin] = deal(E4{:});
%     E5 = num2cell(epAC);
%     [EEG.epoch.accuracy] = deal(E5{:});
%     E6 = num2cell(epCL);
%     [EEG.epoch.clarityOrig] = deal(E6{:});
%     E7 = num2cell(epCB);
%     [EEG.epoch.clarityBin] = deal(E7{:});

    
    % REMOVE MISSING TRIALS AND SAVE
    IDX = find(isnan(cell2mat({EEG.epoch.trialIDX})));
    
    EEG = pop_select(EEG,'notrial',IDX);
    
    EEG.setname = ['s' num2str(sbj) '_DiN_final_wTrialInfo'];
    
    pop_saveset(EEG,'filename',[EEG.setname '.set'],...
        'filepath',outDir);
    
    trial_IDX = epTR;
    trial_IDX(IDX) = [];
%     digit_ID = epDI;
%     digit_ID(IDX) = [];
%     ITI = epIT;
%     ITI(IDX) = [];
%     deg_lvl = epDL;
%     deg_lvl(IDX) = [];
%     deg_bin = epDB;
%     deg_bin(IDX) = [];
%     accuracy = epAC;
%     accuracy(IDX) = [];
%     clarity = epCL;
%     clarity(IDX) = [];
%     clarityBin = epCB;
%     clarityBin(IDX) = [];
    
    diary([outDir 'epochDiary.txt'])
   disp(['N TOTAL EPOCH = ' num2str(length(trial_IDX))]);
   disp(['N MISSING EPOCH (incl. cleanArtifact rejected) = '...
       num2str(378 - length(trial_IDX))]);
    diary off
    
    % REREFERENCE
    EEG = pop_reref(EEG,[]);
    [ALLEEG, EEG, CURRENTSET] = pop_newset(ALLEEG, EEG, CURRENTSET,'setname',...
        ['s' num2str(sbj) '_DiN_final_wTrialInfo_reref'], ...
        'savenew',[outDir 's' num2str(sbj) '_DiN_downsamp_filt_epoched_cleanChan_reref.set']);
    % EEG.setname = ['s' num2str(subject) '_TASK_down_HPF_LPF_cleanEpochsAndChans_interp_reref_cleaning'];
    % EEG.filename = [EEG.setname '.set'];
    [ALLEEG, EEG] = eeg_store(ALLEEG,EEG, CURRENTSET);
    EEG = eeg_checkset(EEG);
    eeglab redraw
    
%     EEGbak = EEG;
    
    
    % REMOVE BAD EPOCHS
% %     timeRange = 1:650;  % time range for cleaning = -3.4 to -0.1 sec
    timeRange = 1:840;   % time range for cleaning = -4.3 to -0.1 sec

    % Finds the difference between the maximum and minimum of each epoch.
    diffs = squeeze( max(EEG.data(:,timeRange,:),[],2) - min(EEG.data(:,timeRange,:),[],2) );
%         diffs = squeeze( max(EEG.data,[],2) - min(EEG.data,[],2) );

    % We'll kick out any trials whose difference exceeds this uV threshhold
    threshold = 200;
    
    % nBadEpochs = 1000;
    k = 1;
    while k
        % Find samples that exceed the threshhold
        [chanidx, epochidx] = find( diffs > threshold );
        
        % Find epochs that have at least one sample, at any channel, exceeding the
        % threshhold
        nBadEpochs = length(unique(epochidx));
        
        disp(['MAXMIN CRITERION THRESHOLD = ' num2str(threshold)...
            ': N bad epochs = ' num2str(nBadEpochs)]);
        
        if nBadEpochs > 100
            threshold = threshold + 50;
        else
            k = 0;
        end
    end
    badepochs.maxmin = unique(epochidx);
    
    diary([outDir 'epochDiary.txt'])
   disp(['MAXMIN CRITERION THRESHOLD = ' num2str(threshold) ...
       ': N bad epochs = ' num2str(nBadEpochs)]);
    diary off
    
    %%% NEIGHBORING SAMPLES CRITERION
    
    % Find the difference between neighboring samples each pair of
    % neighboring samples
    EEGdataCleaning = EEG.data(:,timeRange,:);
    
    diffs = arrayfun( @(x)( squeeze (EEGdataCleaning(:,x,:) - EEGdataCleaning(:,x-1,:) ) ...
        ), 2:size(EEGdataCleaning,2), 'UniformOutput', false );
%     
%     diffs = arrayfun( @(x)( squeeze (EEG.data(:,x,:) - EEG.data(:,x-1,:) ) ...
%         ), 2:size(EEG.data,2), 'UniformOutput', false );
    
    % organize that cell array into a matrix, which will be easier to work with
    n_chan = size(diffs{1},1);
    n_samp = length(diffs);
    n_trial = size(diffs{1},2);
    diffs = reshape(cell2mat(diffs), n_chan, n_samp, n_trial);
    
    % get the max difference across samples, for each trial
    diffs = squeeze( max(diffs,[],2) );
    
    % We'll kick out any trials whose difference exceeds this uV threshhold
    threshold = 75;
    k = 1;
    while k
        % Find samples that exceed the threshhold
        [chanidx, epochidx] = find( diffs > threshold );
        
        % Find epochs that have at least one sample, at any channel, exceeding the
        % threshhold
        nBadEpochs = length(unique(epochidx));
        
        disp(['NEIGHBORING SAMPLES THRESHOLD = ' num2str(threshold)...
            ': N bad epochs = ' num2str(nBadEpochs)]);
        
        if nBadEpochs > 100
            threshold = threshold + 25;
        else
            k = 0;
        end
    end

    % Find epochs that have at least one sample, at any channel, exceeding the
    % threshhold
    
    badepochs.neighbsamp = unique(epochidx);
      
    badEpochs = unique([badepochs.neighbsamp ; badepochs.maxmin]);
    
    diary([outDir 'epochDiary.txt'])
   disp(['NEIGHBORING SAMPLES THRESHOLD = ' ...
       num2str(threshold) ': N bad epochs = ' ...
       num2str(nBadEpochs)]);
    disp(['TRIALS REMOVED (maxMin + neighbSamples) = ' ...
        num2str(length(badEpochs))]);
    diary off

    rejEpochVec = zeros([length(EEG.epoch) 1]);
    rejEpochVec(badEpochs) = 1;
    EEG = pop_rejepoch(EEG, rejEpochVec, 0);
    [ALLEEG, EEG, CURRENTSET] = pop_newset(ALLEEG, EEG, CURRENTSET, 'overwrite','on');
    EEG = eeg_checkset(EEG);
    EEG.setname = ['s' num2str(sbj) '_DiN_final_clean'];
    [ALLEEG, EEG] = eeg_store(ALLEEG,EEG, CURRENTSET);
    eeglab redraw
    
    pop_saveset(EEG,'filename',[EEG.setname '.set'],'filepath',outDir)
    
    %
    nBlocks = 6;
    
    DIGIT_ID = [];
    ITI = [];
    ACCURACY = [];
    DEGRAD_LVL_ORIG = [];
    CLARITY_ORIG = [];
    
    for block = 1:nBlocks
        load([behavDir 'BLOCK_' num2str(block) '/SiN_block_' num2str(block) '_DATA.mat']); % [DATA]
        DIGIT_ID = [DIGIT_ID ; (cell2mat({DATA{:,9}}))'];
        ITI = [ITI ; (round(cell2mat({DATA{:,8}}),1))'];
        DEGRAD_LVL_ORIG = [DEGRAD_LVL_ORIG ; (cell2mat({DATA{:,11}}))'];
        ACCURACY = [ACCURACY ; (cell2mat({DATA{:,7}}))'];
        CLARITY_ORIG = [CLARITY_ORIG ; (cell2mat({DATA{:,5}}))'];
    end
    
    [CLARITYgroups,FORMULA,BOUNDARIES,CLARITY3lvls] = recodeCLARITY(CLARITY_ORIG);
    
     DEGRAD_3_LVL = NaN([378 1]);
    tab = readtable([behavDir 'DiNdataClean.csv'],'ReadVariableNames',0);
    
    deg3lvl = str2double(table2array(tab(:,5)));
    idx_block = str2double(table2array(tab(:,2)));
    idx_trialBlock = str2double(table2array(tab(:,3)));
    
    deg3lvl = deg3lvl(2:end);
    idx_block = idx_block(2:end);
    idx_trialBlock = idx_trialBlock(2:end);
    
    for i = 1:length(deg3lvl)
        trialIDdeg(i) = idx_trialBlock(i) + ((idx_block(i) -1) * 63);
    end
    
    for i = 1:length(deg3lvl)
        DEGRAD_3_LVL(trialIDdeg(i)) = deg3lvl(i);
    end
    
    epTR = cell2mat({EEG.epoch.trialIDX});
    
       diary([outDir 'epochDiary.txt'])
   disp(['FINAL NR EPOCHS RETAINED = ' ...
        num2str(length(epTR))]);
    diary off
    
    epDI = DIGIT_ID(epTR);
    epIT = ITI(epTR);
    epDL = DEGRAD_LVL_ORIG(epTR);
    epDB = DEGRAD_3_LVL(epTR);
    epAC = ACCURACY(epTR);
    epCL = CLARITY_ORIG(epTR);
    epCB = CLARITY3lvls(epTR);
    
    save([outDir 'trialIDX.mat'], 'epTR', 'epIT', 'epDL', 'epDB', ...
        'epAC', 'epCL', 'epCB');
    
    E0 = num2cell(epTR);
    [EEG.epoch.trialIDX] = deal(E0{:});
    E1 = num2cell(epDI);
    [EEG.epoch.digitID] = deal(E1{:});
    E2 = num2cell(epIT);
    [EEG.epoch.ITI] = deal(E2{:});
    E3 = num2cell(epDL);
    [EEG.epoch.degLvlOrig] = deal(E3{:});
    E4 = num2cell(epDB);
    [EEG.epoch.degBin] = deal(E4{:});
    E5 = num2cell(epAC);
    [EEG.epoch.accuracy] = deal(E5{:});
    E6 = num2cell(epCL);
    [EEG.epoch.clarityOrig] = deal(E6{:});
    E7 = num2cell(epCB);
    [EEG.epoch.clarityBin] = deal(E7{:});

    
    
    
    
    
     %% 10) Epoch
        
    disp('---------------------------------------------------------------')
    disp('------------------------- EPOCHING ----------------------------')
    disp('---------------------------------------------------------------')
    
    % trials with less than 4.3 seconds of clean data prior to
    % comprehension response onset are discarded
    EEG = pop_epoch(EEG, {'DI24'}, [-4.3  1], 'newname', ... 
        ['sbj_' num2str(sbj) '_DiN_epoched.set'], ...
        'epochinfo', 'yes');
    EEG = eeg_checkset(EEG);
    [ALLEEG EEG CURRENTSET] = eeg_store(ALLEEG, EEG, CURRENTSET);
    eeglab redraw
 

    pop_saveset(EEG,'filename',EEG.setname,'filepath',outDir)
    
    
    X = {EEG.epoch.eventtype};
    Y = {EEG.epoch.eventurevent};
    Z = NaN([1 length(X)]);
    for i = 1:length(X)
        j = cell2mat(Y{i});
        Xid = find(contains(X{i},'DI24'));
        if length(Xid) == 2
            if ismember(Z(i-1),j)
                Xid = Xid(2);
            elseif sum(ismember(j,cell2mat(Y{i+1}))) > 0
                Xid = Xid(1);
            else
                Xid = Xid(1);
            end
        end     
        Z(i) = j(Xid);
    end
    
    RZ = RESPONSE_IDX(Z);
    NR = find(isnan(RZ));
    if sbj == 18 || sbj == 29
        for i = 1:368
            if ismember(i, NR)
                if (RZ(i-1)) == ((RZ(i+1)) - 2)
                    RZ(i) = (RZ(i-1)) + 1;
                    %                 disp(num2str(i))
                end
            end
        end
    else
        for i = 1:length(RZ)
            if ismember(i, NR)
                if (RZ(i-1)) == ((RZ(i+1)) - 2)
                    RZ(i) = (RZ(i-1)) + 1;
                    %                 disp(num2str(i))
                end
            end
        end
    end
    

    TR = RESPONSE_IDX(Z);

    epTR = NaN([1 length(EEG.epoch)]);

    
    for i = 1:length(EEG.epoch)
        if ~isnan(RZ(i))
            epTR(i) = RZ(i);
        end
    end
    
    E0 = num2cell(epTR);
    [EEG.epoch.trialIDX] = deal(E0{:});

    
    
    %% 11) REMOVE MISSING-RESPONSE TRIALS
    IDX = find(isnan(cell2mat({EEG.epoch.trialIDX})));
    
    EEG = pop_select(EEG,'notrial',IDX);
    
    EEG.setname = ['s' num2str(sbj) '_DiN_final_wTrialInfo'];
    
    pop_saveset(EEG,'filename',[EEG.setname '.set'],...
        'filepath',outDir);
    
    trial_IDX = epTR;
    trial_IDX(IDX) = [];

    
    diary([outDir 'epochDiary.txt'])
   disp(['N TOTAL EPOCH = ' num2str(length(trial_IDX))]);
   disp(['N MISSING EPOCH (incl. cleanArtifact rejected) = '...
       num2str(378 - length(trial_IDX))]);
    diary off
  

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    %% 12) REMOVE BAD EPOCHS
    % this can easily be skipped
    
% %     timeRange = 1:650;  % time range for cleaning = -3.4 to -0.1 sec
% probably, this was better
    timeRange = 1:840;   % time range for cleaning = -4.3 to -0.1 sec

    % Finds the difference between the maximum and minimum of each epoch.
    diffs = squeeze( max(EEG.data(:,timeRange,:),[],2) - min(EEG.data(:,timeRange,:),[],2) );

    % We'll kick out any trials whose difference exceeds this uV threshhold
    threshold = 200;
    
%     k = 1;
%     while k
        % Find samples that exceed the threshhold
        [chanidx, epochidx] = find( diffs > threshold );
        
        % Find epochs that have at least one sample, at any channel, exceeding the
        % threshhold
        nBadEpochs = length(unique(epochidx));
        
        disp(['MAXMIN CRITERION THRESHOLD = ' num2str(threshold)...
            ': N bad epochs = ' num2str(nBadEpochs)]);
        
%         if nBadEpochs > 100
%             threshold = threshold + 50;
%         else
%             k = 0;
%         end
%     end
    badepochs.maxmin = unique(epochidx);
    
    diary([outDir 'epochDiary.txt'])
   disp(['MAXMIN CRITERION THRESHOLD = ' num2str(threshold) ...
       ': N bad epochs = ' num2str(nBadEpochs)]);
    diary off
    
    %%% NEIGHBORING SAMPLES CRITERION
    
    % Find the difference between neighboring samples each pair of
    % neighboring samples
    EEGdataCleaning = EEG.data(:,timeRange,:);
    
    diffs = arrayfun( @(x)( squeeze (EEGdataCleaning(:,x,:) - EEGdataCleaning(:,x-1,:) ) ...
        ), 2:size(EEGdataCleaning,2), 'UniformOutput', false );
%     
%     diffs = arrayfun( @(x)( squeeze (EEG.data(:,x,:) - EEG.data(:,x-1,:) ) ...
%         ), 2:size(EEG.data,2), 'UniformOutput', false );
    
    % organize that cell array into a matrix, which will be easier to work with
    n_chan = size(diffs{1},1);
    n_samp = length(diffs);
    n_trial = size(diffs{1},2);
    diffs = reshape(cell2mat(diffs), n_chan, n_samp, n_trial);
    
    % get the max difference across samples, for each trial
    diffs = squeeze( max(diffs,[],2) );
    
    % We'll kick out any trials whose difference exceeds this uV threshhold
    threshold = 75;
%     k = 1;
%     while k
        % Find samples that exceed the threshhold
        [chanidx, epochidx] = find( diffs > threshold );
        
        % Find epochs that have at least one sample, at any channel, exceeding the
        % threshhold
        nBadEpochs = length(unique(epochidx));
        
        disp(['NEIGHBORING SAMPLES THRESHOLD = ' num2str(threshold)...
            ': N bad epochs = ' num2str(nBadEpochs)]);
        
%         if nBadEpochs > 100
%             threshold = threshold + 25;
%         else
%             k = 0;
%         end
%     end

    % Find epochs that have at least one sample, at any channel, exceeding the
    % threshhold
    
    badepochs.neighbsamp = unique(epochidx);
      
    badEpochs = unique([badepochs.neighbsamp ; badepochs.maxmin]);
    
    diary([outDir 'epochDiary.txt'])
   disp(['NEIGHBORING SAMPLES THRESHOLD = ' ...
       num2str(threshold) ': N bad epochs = ' ...
       num2str(nBadEpochs)]);
    disp(['TRIALS REMOVED (maxMin + neighbSamples) = ' ...
        num2str(length(badEpochs))]);
    diary off

    rejEpochVec = zeros([length(EEG.epoch) 1]);
    rejEpochVec(badEpochs) = 1;
    EEG = pop_rejepoch(EEG, rejEpochVec, 0);
    [ALLEEG, EEG, CURRENTSET] = pop_newset(ALLEEG, EEG, CURRENTSET, 'overwrite','on');
    EEG = eeg_checkset(EEG);
    EEG.setname = ['s' num2str(sbj) '_DiN_final_clean'];
    [ALLEEG, EEG] = eeg_store(ALLEEG,EEG, CURRENTSET);
    eeglab redraw
    
    pop_saveset(EEG,'filename',[EEG.setname '.set'],'filepath',outDir)
    
    
    
    
    
    
    
    
    %
    nBlocks = 6;
    
    DIGIT_ID = [];
    ITI = [];
    ACCURACY = [];
    DEGRAD_LVL_ORIG = [];
    CLARITY_ORIG = [];
    
    for block = 1:nBlocks
        load([behavDir 'BLOCK_' num2str(block) '/SiN_block_' num2str(block) '_DATA.mat']); % [DATA]
        DIGIT_ID = [DIGIT_ID ; (cell2mat({DATA{:,9}}))'];
        ITI = [ITI ; (round(cell2mat({DATA{:,8}}),1))'];
        DEGRAD_LVL_ORIG = [DEGRAD_LVL_ORIG ; (cell2mat({DATA{:,11}}))'];
        ACCURACY = [ACCURACY ; (cell2mat({DATA{:,7}}))'];
        CLARITY_ORIG = [CLARITY_ORIG ; (cell2mat({DATA{:,5}}))'];
    end
    
    [CLARITYgroups,FORMULA,BOUNDARIES,CLARITY3lvls] = recodeCLARITY(CLARITY_ORIG);
    
     DEGRAD_3_LVL = NaN([378 1]);
    tab = readtable([behavDir 'DiNdataClean.csv'],'ReadVariableNames',0);
    
    deg3lvl = str2double(table2array(tab(:,5)));
    idx_block = str2double(table2array(tab(:,2)));
    idx_trialBlock = str2double(table2array(tab(:,3)));
    
    deg3lvl = deg3lvl(2:end);
    idx_block = idx_block(2:end);
    idx_trialBlock = idx_trialBlock(2:end);
    
    for i = 1:length(deg3lvl)
        trialIDdeg(i) = idx_trialBlock(i) + ((idx_block(i) -1) * 63);
    end
    
    for i = 1:length(deg3lvl)
        DEGRAD_3_LVL(trialIDdeg(i)) = deg3lvl(i);
    end
    
    epTR = cell2mat({EEG.epoch.trialIDX});
    
       diary([outDir 'epochDiary.txt'])
   disp(['FINAL NR EPOCHS RETAINED = ' ...
        num2str(length(epTR))]);
    diary off
    
    epDI = DIGIT_ID(epTR);
    epIT = ITI(epTR);
    epDL = DEGRAD_LVL_ORIG(epTR);
    epDB = DEGRAD_3_LVL(epTR);
    epAC = ACCURACY(epTR);
    epCL = CLARITY_ORIG(epTR);
    epCB = CLARITY3lvls(epTR);
    
    save([outDir 'trialIDX.mat'], 'epTR', 'epIT', 'epDL', 'epDB', ...
        'epAC', 'epCL', 'epCB');
    
    E0 = num2cell(epTR);
    [EEG.epoch.trialIDX] = deal(E0{:});
    E1 = num2cell(epDI);
    [EEG.epoch.digitID] = deal(E1{:});
    E2 = num2cell(epIT);
    [EEG.epoch.ITI] = deal(E2{:});
    E3 = num2cell(epDL);
    [EEG.epoch.degLvlOrig] = deal(E3{:});
    E4 = num2cell(epDB);
    [EEG.epoch.degBin] = deal(E4{:});
    E5 = num2cell(epAC);
    [EEG.epoch.accuracy] = deal(E5{:});
    E6 = num2cell(epCL);
    [EEG.epoch.clarityOrig] = deal(E6{:});
    E7 = num2cell(epCB);
    [EEG.epoch.clarityBin] = deal(E7{:});

    
    
    %% 11) REMOVE TRIALS WITH NO RESPONSE
        
    disp('---------------------------------------------------------------')
    disp('-------------- REMOVING TRIALS WITH NO RESPONSE ---------------')
    disp('---------------------------------------------------------------')
    
    behavDir = [thisPath '/SUBJECT_' num2str(sbj) '/DiN/'];
    nBlocks = 6;
    
    digitReported = [];
    for block = 1:nBlocks
        load([behavDir 'BLOCK_' num2str(block) '/SiN_block_' num2str(block) '_DATA.mat']); % [DATA]
        digitReported = [digitReported ; (str2double({DATA{:,3}}))'];
    end
    
    noRespTrial = find(isnan(digitReported));
    noRespTrialIDX = NaN(size(noRespTrial));
    for i = 1:length(noRespTrial)
        if ~isempty(find(cell2mat({EEG.epoch.trialIDX}) == noRespTrial(i)))
            noRespTrialIDX(i) = find(cell2mat({EEG.epoch.trialIDX}) == noRespTrial(i));
        end
    end
    
%     if sbj == 22
%         noRespTrialIDX(1) = []; % this epoch was removed previously
%     end
    
    EEG.noRespEpoch = noRespTrialIDX;
    
    EEG = pop_selectevent(EEG, 'omitepoch',noRespTrialIDX,...
        'deleteevents','off','deleteepochs','on','invertepochs','off');
    
    pop_saveset(EEG,'filename',[EEG.setname '_Zscored.set'],'filepath',outDir);
    
    trial_IDX = cell2mat({EEG.epoch.trialIDX});
    digID = cell2mat({EEG.epoch.digitID});
    ITI = cell2mat({EEG.epoch.ITI});
    degLvlOrig = cell2mat({EEG.epoch.degLvlOrig});
    degBin = cell2mat({EEG.epoch.degBin});
    comprehension = cell2mat({EEG.epoch.accuracy});
    clarityOrig = cell2mat({EEG.epoch.clarityOrig});
    clarityBin = cell2mat({EEG.epoch.clarityBin});
    
    save([outDir 'sbj_' num2str(sbj) '_trialInfo_Zscored.mat'], 'trial_IDX', 'digID', ...
        'ITI', 'degLvlOrig', 'degBin', 'comprehension', 'clarityOrig', 'clarityBin','backupEvents');
    
    
    
    %% 13) RUN ICA & REMOVE NON-BRAIN COMPONENTS
        
    disp('---------------------------------------------------------------')
    disp('------------------------ RUNNING ICA --------------------------')
    disp('---------------------------------------------------------------')
    
    
    EEG = pop_runica(EEG, 'icatype', 'runica', 'extended',1,'interrupt','on');
    [ALLEEG, EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
    EEG = eeg_checkset(EEG);
    eeglab redraw
    
    addpath('/p01-hdd/dsa/thouwe-srv/eeglab2020_0/plugins/firfilt2.3/firfilt-2.4/');
    EEG = iclabel(EEG);
    
    
    % initialize ica data
    maxsamp = 1e5;
    n_samp = min(maxsamp, EEG.pnts*EEG.trials);
    scalpDataVarExplained = NaN([size(EEG.icaact,1) 1]);
    
    for comp = 1:size(EEG.icaact,1)
        
        if ~isempty(EEG.icaact)
            icaacttmp = EEG.icaact(comp, :, :);
        else
            icaacttmp  = eeg_getdatact(EEG, 'component', chanorcomp);
        end
        
        try
            samp_ind = randperm(EEG.pnts*EEG.trials, n_samp);
        catch
            samp_ind = randperm(EEG.pnts*EEG.trials);
            samp_ind = samp_ind(1:n_samp);
        end
        if ~isempty(EEG.icachansind)
            icachansind = EEG.icachansind;
        else
            icachansind = 1:EEG.nbchan;
        end
        datavar = mean(var(EEG.data(icachansind, samp_ind), [], 2));
        
        projvar = mean(var(EEG.data(icachansind, samp_ind) - ...
            EEG.icawinv(:, comp) * icaacttmp(1, samp_ind), [], 2));
        scalpDataVarExplained(comp) = 100 *(1 - projvar/ datavar);
    end
    
    
    scalpDataVarExplained_TOT = sum(scalpDataVarExplained);
    
    pop_viewprops( EEG, 0, 1:size(EEG.icaact,1), {'freqrange', [2 48]}, {}, 1, 'ICLabel' )
    EEG = eeg_checkset( EEG );
    
    EEG.IClabel_classification = EEG.etc.ic_classification.ICLabel.classifications;
    EEG.IClabel_classification_classes = EEG.etc.ic_classification.ICLabel.classes;
    
    
    
    if sbj == 3
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [];
    elseif sbj == 4
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [4 7 8 11 15 17 19 22 23 26 28 29 31];
    elseif sbj == 5
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [2 7 8 11 15 21 23];
    elseif sbj == 6
        EEG.IClabel_added = []; 
        EEG.IClabel_brainRemoved = [1 8:10 29 30]; 
    elseif sbj == 7
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [1 8];
    elseif sbj == 8
        EEG.IClabel_added = 11;
        EEG.IClabel_brainRemoved = [];
    elseif sbj == 9
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [];
    elseif sbj == 10
        EEG.IClabel_added = 9;
        EEG.IClabel_brainRemoved = [];
    elseif sbj == 11
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [23 86];
    elseif sbj == 12
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [14 21];
    elseif sbj == 13
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [];
    elseif sbj == 14
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = 6;
    elseif sbj == 15
        EEG.IClabel_added = [7 16];
        EEG.IClabel_brainRemoved = [2 8 15 24];
    elseif sbj == 16
        EEG.IClabel_added = 7;
        EEG.IClabel_brainRemoved = [5 11];
    elseif sbj == 17
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [4 5 18];
    elseif sbj == 18
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [];
    elseif sbj == 19
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = 12;
    elseif sbj == 20
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [6 9 11];
    elseif sbj == 21
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = 14;
    elseif sbj == 22
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = 14;
    elseif sbj == 23
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [];
    elseif sbj == 24
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [];
    elseif sbj == 25
        EEG.IClabel_added = []; 
        EEG.IClabel_brainRemoved = []; 
    elseif sbj == 26
        EEG.IClabel_added = 10;
        EEG.IClabel_brainRemoved = 26;
    elseif sbj == 27
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [2 28]; 
    elseif sbj == 28
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = 13;
    elseif sbj == 29
        EEG.IClabel_added = []; 
        EEG.IClabel_brainRemoved = 8:10;
    elseif sbj == 30
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = 6;
    elseif sbj == 31
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [];
    elseif sbj == 32
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [1 2 10];
    elseif sbj == 33
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [];
    elseif sbj == 35
        EEG.IClabel_added = 2;
        EEG.IClabel_brainRemoved = [];
    elseif sbj == 36
        EEG.IClabel_added = 9;
        EEG.IClabel_brainRemoved = [];
    elseif sbj == 37
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [2 3 6 11 16];
    elseif sbj == 38
        EEG.IClabel_added = [];
        EEG.IClabel_brainRemoved = [1 13 20];
    end
    
    removeComp = zeros([size(EEG.IClabel_classification,1) 1]);
    for comp = 1:size(EEG.IClabel_classification,1)
        [Y,I] = max(EEG.IClabel_classification(comp,:));
        if I ~= 1
            removeComp(comp) = 1;
        end
        if ismember(comp,EEG.IClabel_added)
            removeComp(comp) = 0;
        end
        if ismember(comp,EEG.IClabel_brainRemoved)
            removeComp(comp) = 1;
        end
    end
    
    EEG.IClabel_compRemoved = find(removeComp);
    EEG.IClabel_compRetained = setdiff(1:size(EEG.IClabel_classification,1),EEG.IClabel_compRemoved);
    
    
    EEG.scalpDataVarExplained = scalpDataVarExplained;
    EEG.scalpDataVarExplained_TOT = scalpDataVarExplained_TOT;
    EEG.scalpDataVarExplained_compRetained = sum(scalpDataVarExplained(EEG.IClabel_compRetained));
    EEG.scalpDataVarExplained_compRemoved = sum(scalpDataVarExplained(EEG.IClabel_compRemoved));
    
    
    EEG=pop_subcomp(EEG, EEG.IClabel_compRemoved, 0);
    
    EEG.setname = ['s' num2str(sbj) '_DiN_epoched_ICrem'];
    [ALLEEG, EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
    EEG = eeg_checkset(EEG);
    eeglab redraw
    
    pop_saveset(EEG,'filename',[EEG.setname '.set'],'filepath',outDir)
    
    
    close all;
end

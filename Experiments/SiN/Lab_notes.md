# LIRI Lab notes
## Audio profile
### RME TotalMix Interface
(click icon on windows task bar)
- Software playback  An1 is routed to hardware outputs Phones 1 and 2
- Phones 1 are the headphones outside booth
- Phones 2 are the headphones inside booth 
- Software playback An2 goes to Hardware AN7 (this is connected to Erg 1 in biosemi amp)

See **sin_audio_snapshot.tss** for RME total mix audio settings:
- Volume in Hardware output An7 and software playback An2 volume is set at 0. Don't change or threshold for trigger in Biosemi will be affected!
- Volume in software playback An1 at set at lowest

### Testing PTA

~10 min. Pure tone audiometry
Uses Thinkpad audiometry laptop. Requires manual adjustment/ testing with ext headpphones in the booth
Participant data should be manually entered , e.g., Redcap 

### Audio settings
- Analog 1/2 should be selected in windows audio and Psychopy

## Misc
-	Make sure Audio device box is turned on before oepning Psychopy
-	Parallel port is : 3FE8
-	When starting File in Biosemi actiview tick the box ‘Add displayed sensors’. Select sensor ERG 1  (this is for the audio signal that is sent to the amplifier)

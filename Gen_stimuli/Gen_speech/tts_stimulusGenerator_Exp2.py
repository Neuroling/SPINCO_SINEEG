#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create stimuli-parts using google's text to speech API
===============================================================================
Created on Thu Apr 25 09:34:13 2024
@author: samuemu

This will create the stimuli as single words, and also "Vorsicht", "gehe sofot zum", "Feld der Spalte"
These will then be stitched together in "tts_singleStimuli2sentence.py" into the
stimulus sentences. This is done to keep the coarticulation of the common parts constant.

INSTRUCTIONS:
-------------
Read the instructions fully before starting.

To run this script, you first need to go to Link1 to set up an account with Google Cloud.
It is free (as of April 2024) but requires credit card information to prove you're human.
It should automatically create a project, but if not, create a project.

Then, go to Link2 for instructions to install the python client. In Linux, it is
running the following code in the terminal:
```
python3 -m venv <your-env>
source <your-env>/bin/activate
pip install google-cloud-texttospeech
```

Then, go to Link3 for instructions to install the gcloud CLI. You might need to 
log into google when prompted.
Then, go to Link4 for instructions on how to authenticate your credentials. Again, when prompted,
log into your google account.

If at any point you get a message to activate your project, follow the link they provide
in the message and activate your project.

After all this is done, while still in the console and with the environment active, 
navigate to the folder where this script is saved and run it with the line
`python3 tts_stimulusGenerator_Exp2.py`

Unfortunately, it will save all outputs in the same folder as the script is saved. 
Drag them over into the folder you want them in afterwards.


Link1 : https://cloud.google.com/text-to-speech/?hl=en
Link2 : https://cloud.google.com/python/docs/reference/texttospeech/latest
Link3 : https://cloud.google.com/sdk/docs/install#linux
Link4 : https://cloud.google.com/docs/authentication/provide-credentials-adc#how-to
"""


import google.cloud.texttospeech as tts



stimuli = ['Adler','Rabe','Eule', 'Tiger','Ratte', 
         'Esel', 'Kaefer', 'Spinne', 'Biene',
         'Hammer', 'Nagel', 'Schraube',
         'Jacke', 'Mantel', 'Hose',
         'Fahrrad', 'Flugzeug', 'Auto', 'Velo',
         'Becher', 'Teller', 'Tasse', 'Messer', 'Pfanne', 'Gabel', 'Loeffel',
         'Kissen', 'Teppich', 'Fenster', 'Sessel', 'Sofa',
         'gelben','gruenen','roten','weissen', 'blauen', 
         'schwarzen', 'pinken', 'braunen', 'grauen',
         'Eins','Zwei','Drei','Vier', 'Fuenf', 'Sechs', 'Acht', 'Neun',
         'Vorsicht', 'gehe sofort zum', 'Feld der Spalte']

lang_voice_speaker = ['de-DE-Neural2-D',
            'de-DE-Neural2-F']



def text_to_wav(voice_name: str, text: str, outputname: str):
        language_code = "-".join(voice_name.split("-")[:2]) 
        text_input = tts.SynthesisInput(text=text)
        voice_params = tts.VoiceSelectionParams(language_code=language_code, name=voice_name)
        audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16,
                        sample_rate_hertz=48000)
        client = tts.TextToSpeechClient()     
        response = client.synthesize_speech(input=text_input, voice=voice_params, audio_config=audio_config)
        outputname = outputname + ".wav"
        with open(outputname, "wb") as out:
            out.write(response.audio_content)
            print("Generated speech saved to " + outputname + ".wav")
		
for i,text in enumerate(stimuli):
    for voice_name in lang_voice_speaker:
        #Make informative outputname 
        variationLabel = text[:4]   # Code which from the changing words were contained in the sentence (e.g., Ad-ge-Ei ) 
        voiceLabel  = voice_name.replace('de-DE-','DE_')
        filename = voiceLabel + '_' +  variationLabel        
        # print(filename)
        # outputname = os.path.join(diroutput,filename)
        outputname = filename
        text_to_wav(voice_name,text,outputname)
        with open(outputname+".txt", "w") as file:
                  file.write(text)
        
        

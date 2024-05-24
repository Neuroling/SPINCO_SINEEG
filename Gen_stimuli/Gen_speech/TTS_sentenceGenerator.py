"""
create stimuli using google's text to speech API
===============================================================================
@author: gfraga & samuemu

This script uses the google cloud text-to-speech API to generate stimuli. 

For instructions on how to set up the google cloud TTS API, please see the README file
saved in the same directory as this script
"""


import google.cloud.texttospeech as tts
import os
# %%

# Sentence variations 
sentence = 'Vorsicht xnamex, geh sofort zum xcolourx Faeld von der Spalte xnumberx'

callSigns = ['Messer', 'Gabel', 'Teller', 'Loeffel', 'Velo','Adler','Eule', 'Tiger','Ratte', 'Hammer',  'Schraube', 'Flugzeug', 'Auto', 'Fahrrad']
# callSigns = ['Adler','Eule', 'Tiger','Ratte', 'Hammer',  'Schraube', 'Flugzeug', 'Auto']

colours = ['gelben','gruenen','roten','weissen', 'blauen', 
         'schwarzen', 'pinken', 'braunen']

# numbers = ['Eins','Zwei','Drei','Vier', 'Fuenf', 'Sechs', 'Acht', 'Neun']
numbers = ['Null','Eins','Zwei','Drei','Vier', 'Fuenf', 'Sechs', 'Acht', 'Neun']

sentence_version = [sentence.replace("xnamex", callSign).replace("xcolourx", colour).replace("xnumberx", number)         
           for callSign in callSigns for colour in colours for number in numbers]

lang_voice_speaker = [
    # 'de-DE-Neural2-D',
    'de-DE-Neural2-F'
            ]
#lang_voice_speaker = ['de-DE-Wavenet-F']
 

def text_to_wav(voice_name: str, text: str, outputname: str):
        language_code = "-".join(voice_name.split("-")[:2]) 
        text_input = tts.SynthesisInput(text=text)
        voice_params = tts.VoiceSelectionParams(language_code=language_code, name=voice_name)
        audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16,
                        sample_rate_hertz=48000)
        client = tts.TextToSpeechClient()     
        response = client.synthesize_speech(input=text_input, voice=voice_params, audio_config=audio_config)
        filename = outputname + ".wav"
        with open(filename, "wb") as out:
            out.write(response.audio_content)
            print("Generated speech saved to " + filename)
		
for i,text in enumerate(sentence_version):
    for voice_name in lang_voice_speaker:
        #Make informative outputname 
        variationLabel = "-".join([text.split()[j][:3] for j in [1, 5, 10]]) 
        # Code which from the changing words were contained in the sentence (e.g., Ad-ge-Ei ) 
        voiceLabel  = voice_name.replace('de-DE-','DE_')
        outputname = voiceLabel + '_' +  variationLabel
        
        # print(outputname)
        text_to_wav(voice_name,text,outputname)
        with open(outputname+".txt", "w") as file:
                  file.write(text)
        
        

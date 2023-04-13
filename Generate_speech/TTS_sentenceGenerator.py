import google.cloud.texttospeech as tts
import os
# %%

# Sentence variations 
sentence = 'Vorsicht xnamex, geh sofort zum xcolorx Faeld von der Spalte xnumberx'
names = ['Adler','Drossel','Tiger','Kröte']
colors = ['gelben','gruenen','roten','weissen']
numbers = ['Eins','Zwei','Drei','Vier']


sentence_version = [sentence.replace("xnamex", name).replace("xcolorx", color).replace("xnumberx", number)         
           for name in names for color in colors for number in numbers]

lang_voice_speaker = ['de-DE-Neural2-D',
            'de-DE-Neural2-F']
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
        variationLabel = "-".join([text.split()[j][:2] for j in [1, 5, 10]])        # Code which from the changing words were contained in the sentence (e.g., Ad-ge-Ei ) 
        voiceLabel  = voice_name.replace('de-DE-','DE_')
        outputname = voiceLabel + '_' +  variationLabel
        
        #print(outputname)
        text_to_wav(voice_name,text,outputname)
        with open(outputname+".txt", "w") as file:
                 file.write(text)
        
        
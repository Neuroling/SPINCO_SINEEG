import google.cloud.texttospeech as tts
import os


# Sentence variations 
sentence = 'Vorsicht xnamex, gang sofort zum xcolorx Fäld vo de Spalte xnumberx'
names = ['Adler','Drossel','Tiger','Unke']
colors = ['Gelb','Gruen','Rot','Weiss']
numbers = ['Eins','Zwei','Drei','Vier']


sentence_version = [sentence.replace("xnamex", name).replace("xcolorx", color).replace("xnumberx", number)         
           for name in names for color in colors for number in numbers]



lang_voice_speaker = ['de-DE-Neural2-D',
            'de-DE-Neural2-F',
            'de-DE-Wavenet-A',
            'de-DE-Wavenet-A',
            'de-DE-Wavenet-B',
            'de-DE-Wavenet-C',
            'de-DE-Wavenet-D',
            'de-DE-Wavenet-E',
            'de-DE-Wavenet-F']
lang_voice_speaker = ['de-DE-Wavenet-F']

def text_to_wav(voice_name: str, text: str, outputname: str):
        language_code = "-".join(voice_name.split("-")[:2])    
        text_input = tts.SynthesisInput(text=text)
        voice_params = tts.VoiceSelectionParams(language_code=language_code, name=voice_name)
        audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)
        client = tts.TextToSpeechClient()
        response = client.synthesize_speech(input=text_input, voice=voice_params, audio_config=audio_config)    
        filename = f"{outputname}.wav"
        with open(filename, "wb") as out:
            out.write(response.audio_content)
            print(f'Generated speech saved to "{filename}"')
		
 
for i,text in enumerate(sentence_version):
    for voice_name in lang_voice_speaker:
        outputname = "s{:02d}".format(i+1)+'_' + voice_name
        #print(outputname)
        text_to_wav(voice_name,text,outputname)
		
 
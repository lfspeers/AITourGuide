import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import os
import datetime


def text_to_speech(text: str, voice: str) -> None:
    key = os.environ['AI_MULTISERVICE_KEY']
    region = os.environ['AI_MULTISERVICE_REGION']

    
    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    # speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Webm24Khz16BitMonoOpus) # If you need another format
    speech_config.speech_synthesis_voice_name = voice

    now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    outfile = f'audio_files/narration_{now}.wav'

    audio_config = speechsdk.audio.AudioOutputConfig(filename=outfile) # use_default_speaker=True) 
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = synthesizer.speak_text(text)

    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesis failed:", result.error_details)

    return outfile


if __name__ == "__main__": 
    text_to_speech("This is a mic check.", 'en-US-GuyNeural')
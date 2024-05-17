from azure.storage.blob import BlobServiceClient
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioDataStream, ResultReason
import os
import uuid
from celery import shared_task

@shared_task
def generate_audio_and_save_to_blob(text, note_id, container_name, blob_connection_string, azure_region, azure_tts_key):
    speech_config = SpeechConfig(subscription=azure_tts_key, region=azure_region)
    synthesizer = SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async(text).get()

    if result.reason == ResultReason.SynthesizingAudioCompleted:
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
        if 'notestore' in container_name.lower():
            prefix = 'notestore'
        elif 'booknote' in container_name.lower():
            prefix = 'booknote'
        else:
            prefix = 'unknown'
        
        unique_filename = f"{prefix}_{note_id}_{uuid.uuid4()}.wav"
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=unique_filename)
        
        audio_stream = AudioDataStream(result)
        temp_audio_file = f"{prefix}_{note_id}_{uuid.uuid4()}.wav"
        audio_stream.save_to_wav_file(temp_audio_file)
        
        with open(temp_audio_file, "rb") as audio_file:
            blob_client.upload_blob(audio_file)
        
        os.remove(temp_audio_file)
        
        return blob_client.url
    else:
        raise Exception("Error during text-to-speech synthesis")

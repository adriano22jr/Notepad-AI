import azure.ai.textanalytics as text_analytics
import azure.core.credentials as core_credentials
import azure.cognitiveservices.speech as speechsdk
import requests, uuid, app_config

language_key = app_config.LANGUAGE_KEY
language_endpoint = app_config.LANGUAGE_ENDPOINT

translator_key = app_config.TRANSLATOR_KEY
translator_endpoint = app_config.TRANSLATOR_ENDPOINT
translator_location = app_config.TRANSLATOR_LOCATION

speech_key = app_config.SPEECH_KEY
speech_location = app_config.SPEECH_LOCATION

def extract_summarization(text):
    text_analytics_client = text_analytics.TextAnalyticsClient(language_endpoint, core_credentials.AzureKeyCredential(language_key))
    poller = text_analytics_client.begin_abstract_summary(text)
    
    extract_summary_results = poller.result()
    summary = ""
    for result in extract_summary_results:
        if result.kind == "AbstractiveSummarization":
            summary = " ".join([sentence.text for sentence in result.summaries])
        elif result.is_error is True:
            summary = None
    return summary

def translate_text(text, languages: list):
    path = translator_endpoint + "translate"
    params = {'api-version': '3.0', 'to': languages}
    headers = {'Ocp-Apim-Subscription-Key': translator_key, 'Ocp-Apim-Subscription-Region': translator_location, 'Content-type': 'application/json', 'X-ClientTraceId': str(uuid.uuid4())}
    body = [{'text': text}]
    
    request = requests.post(path, params = params, headers = headers, json = body)
    return request.json()

def detect_language(text):
    path = translator_endpoint + "detect"
    params = {'api-version': '3.0'}
    headers = {'Ocp-Apim-Subscription-Key': translator_key, 'Ocp-Apim-Subscription-Region': translator_location, 'Content-type': 'application/json', 'X-ClientTraceId': str(uuid.uuid4())}
    body = [{'text': text}]
    
    request = requests.post(path, params = params, headers = headers, json = body)
    return request.json()

def recognize_speech(language):
    speech_config = speechsdk.SpeechConfig(subscription = speech_key, region = speech_location)
    speech_config.speech_recognition_language = language
    
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone = True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config = speech_config, audio_config = audio_config, language = language)
    
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return speech_recognition_result.text
    else: return None
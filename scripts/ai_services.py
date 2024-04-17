import azure.ai.textanalytics as text_analytics
import azure.core.credentials as core_credentials
import azure.cognitiveservices.speech as speechsdk
import openai
import requests, uuid, app_config

language_key = app_config.LANGUAGE_KEY
language_endpoint = app_config.LANGUAGE_ENDPOINT

translator_key = app_config.TRANSLATOR_KEY
translator_endpoint = app_config.TRANSLATOR_ENDPOINT
translator_location = app_config.TRANSLATOR_LOCATION

speech_key = app_config.SPEECH_KEY
speech_location = app_config.SPEECH_LOCATION

openai_key = app_config.OPENAI_KEY
openai_endpoint = app_config.OPENAI_ENDPOINT
openai_deployment_name = app_config.OPEAI_DEPLOYMENT_NAME

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
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config = speech_config)
    
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return speech_recognition_result.text
    else: return None
    
def generate_text(input_phrase):
    openai_client = openai.AzureOpenAI(azure_endpoint = openai_endpoint, api_key = openai_key, api_version = "2024-02-01")
    
    response = openai_client.completions.create(model = openai_deployment_name, prompt = input_phrase, max_tokens = 250)
    return response.choices[0].text
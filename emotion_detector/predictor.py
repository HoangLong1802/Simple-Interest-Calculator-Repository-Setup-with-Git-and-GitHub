from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class EmotionPredictor:
    def __init__(self, api_key: str, url: str):
        auth = IAMAuthenticator(api_key)
        self.client = NaturalLanguageUnderstandingV1(
            version='2021-08-01',
            authenticator=auth
        )
        self.client.set_service_url(url)

    def predict(self, text: str) -> dict:
        if not text or not text.strip():
            raise ValueError("Input text must not be empty")

        response = self.client.analyze(
            text=text,
            features=Features(emotion=EmotionOptions())
        ).get_result()
        return response['emotion']['document']['emotion']
import pytest
from emotion_detector import EmotionPredictor, format_emotions

API_KEY = 'fake-key'
URL = 'https://fake.watson.url'

class DummyClient:
    def __init__(self, emotion_scores):
        self._scores = emotion_scores

    def analyze(self, text, features):
        class Result:
            def get_result(inner):
                return {'emotion': {'document': {'emotion': self._scores}}}
        return Result()

@pytest.fixture(autouse=True)
def mock_watson(monkeypatch):
    # Monkey-patch the Watson client inside EmotionPredictor
    from emotion_detector.predictor import NaturalLanguageUnderstandingV1, IAMAuthenticator
    monkeypatch.setattr('emotion_detector.predictor.IAMAuthenticator', lambda key: None)
    monkeypatch.setattr('emotion_detector.predictor.NaturalLanguageUnderstandingV1',
                        lambda version, authenticator: DummyClient({
                            'joy': 0.6, 'sadness': 0.1, 'anger': 0.1, 'fear': 0.1, 'disgust': 0.1
                        }))

def test_predict_success():
    predictor = EmotionPredictor(API_KEY, URL)
    result = predictor.predict("I am happy!")
    assert isinstance(result, dict)
    assert all(0 <= v <= 1 for v in result.values())

@pytest.mark.parametrize("input_text", ["", "   "], ids=["empty", "spaces"])
def test_predict_empty(input_text):
    predictor = EmotionPredictor(API_KEY, URL)
    with pytest.raises(ValueError):
        predictor.predict(input_text)

def test_format_emotions():
    data = {'joy': 0.75, 'sadness': 0.10}
    formatted = format_emotions(data)
    assert "Joy: 0.75" in formatted
    assert "Sadness: 0.10" in formatted
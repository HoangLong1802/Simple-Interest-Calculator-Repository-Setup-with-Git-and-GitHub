from flask import Flask, request, jsonify
from emotion_detector import EmotionPredictor, format_emotions
import os

app = Flask(__name__)
api_key = os.getenv('WATSON_API_KEY')
service_url = os.getenv('WATSON_URL')

predictor = EmotionPredictor(api_key, service_url)

@app.route('/detect', methods=['POST'])
def detect_emotion():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing "text" in request'}), 400
    try:
        emotions = predictor.predict(data['text'])
        formatted = format_emotions(emotions)
        return jsonify({'emotions': emotions, 'formatted': formatted}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception:
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
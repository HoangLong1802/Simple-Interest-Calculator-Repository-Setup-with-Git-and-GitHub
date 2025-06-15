from typing import Dict

def format_emotions(emotions: Dict[str, float]) -> str:
    """
    Format the emotion scores into a readable string output.

    Example output:
      Joy: 0.75
      Sadness: 0.10
      Anger: 0.05
      Fear: 0.05
      Disgust: 0.05
    """
    lines = [f"{emotion.capitalize()}: {score:.2f}" for emotion, score in emotions.items()]
    return "\n".join(lines)
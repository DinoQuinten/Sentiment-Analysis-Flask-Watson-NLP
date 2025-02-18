import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze}}

    try:
        
        response = requests.post(url, headers=headers, json=input_json)
        status_code=response.raise_for_status()  # Check for HTTP errors
        result = response.json()

        if status_code == 400:
            return {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None
            }
        
        # Extract emotion data (handling potential missing data)
        emotion_predictions = result.get('emotionPredictions', [])
        if not emotion_predictions:  # Handle the case where there are no predictions
            return {'anger': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'sadness': 0, 'dominant_emotion': 'neutral'}

        emotions_data = emotion_predictions[0].get('emotion', {})  # Get the first prediction's emotions

        emotions = {
            'anger': emotions_data.get('anger', 0),
            'disgust': emotions_data.get('disgust', 0),
            'fear': emotions_data.get('fear', 0),
            'joy': emotions_data.get('joy', 0),
            'sadness': emotions_data.get('sadness', 0)
        }

        dominant_emotion = max(emotions, key=emotions.get)
        emotions['dominant_emotion'] = dominant_emotion

        return emotions

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None
    except (KeyError, TypeError) as e:
        print(f"Parsing Error: {e}. Raw Response: {response.text}")  # Print raw for debugging!
        return None
    except Exception as e: # Catch any other error
        print(f"An unexpected error occurred: {e}")
        return None

# Test the function (this code is only executed when the script is run directly)
if __name__ == "__main__":
    text = "I am so happy I am doing this."
    emotions_result = emotion_detector(text)
    if emotions_result:
        print(emotions_result)
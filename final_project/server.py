from flask import Flask, request, jsonify, render_template
from EmotionDetection import emotion_detector  # Import from your package

app = Flask(__name__, template_folder='/home/project/final_project/oaqjp-final-project-emb-ai/templates/')  # Absolute path

@app.route("/emotionDetector")
def emotion_detector_function():
    text_to_analyze = request.args.get('textToAnalyze')
    response = emotion_detector(text_to_analyze)
    response_text = f"For the given statement, the system response is 'anger': \
                    {response['anger']}, 'disgust': {response['disgust']}, \
                    'fear': {response['fear']}, 'joy': {response['joy']}, \
                    'sadness': {response['sadness']}. The dominant emotion is \
                    {response['dominant_emotion']}."
    print(response_text)
    return response_text

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5002)
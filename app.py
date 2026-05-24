from flask import Flask, render_template, request, jsonify
import joblib
import re
import os
import threading
import webbrowser
import time

app = Flask(__name__)

# Load model and vectorizer (fail gracefully so the server still starts)
model = None
vectorizer = None
try:
    model = joblib.load("phishing_email_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
except Exception as e:
    # Keep running the app but log the error so the user can see why predictions won't work
    print(f"Warning: could not load model or vectorizer: {e}")


# URL feature extraction
def extract_url_count(text):
    urls = re.findall(r'(https?://\S+)', text)
    return len(urls)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    email_text = data["email"]

    # Try lazy-loading the model if it wasn't available at startup
    global model, vectorizer
    if model is None or vectorizer is None:
        try:
            model = joblib.load("phishing_email_model.pkl")
            vectorizer = joblib.load("vectorizer.pkl")
            print("Model and vectorizer loaded on demand")
        except Exception as e:
            print(f"Failed to lazy-load model/vectorizer: {e}")
            return jsonify({
                "error": "Model or vectorizer not loaded. Check server logs." 
            }), 500

    transformed_text = vectorizer.transform([email_text])

    # Prediction
    prediction = model.predict(transformed_text)[0]

    # Probability
    probability = model.predict_proba(transformed_text)[0]

    phishing_prob = round(max(probability) * 100, 2)

    return jsonify({
        "prediction": prediction,
        "confidence": phishing_prob
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
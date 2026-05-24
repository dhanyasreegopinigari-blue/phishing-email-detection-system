import pandas as pd
import re
import joblib
import os
import sys

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

csv_path = os.path.join(os.path.dirname(__file__), 'phishing_email.csv')
print(f"Reading dataset from: {csv_path}")
if not os.path.exists(csv_path):
    print('Error: dataset file not found at', csv_path)
    sys.exit(1)

# Load dataset
data = pd.read_csv(csv_path)

# Features and labels
X = data["text"]
y = data["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(
    stop_words='english',
    lowercase=True
)

# Transform data
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Train model
model = MultinomialNB()
model.fit(X_train_vectorized, y_train)

# Predictions
y_pred = model.predict(X_test_vectorized)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy)

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:\n", cm)

# Classification Report
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# Save model and vectorizer
joblib.dump(model, "phishing_email_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("\nModel and vectorizer saved successfully.")
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Save confusion matrix plot to avoid blocking the script with plt.show()
os.makedirs('screenshots', exist_ok=True)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Phishing', 'Safe'],
            yticklabels=['Phishing', 'Safe'])

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

out_path = os.path.join('screenshots', 'confusion_matrix.png')
plt.savefig(out_path, bbox_inches='tight')
print(f"Saved confusion matrix to {out_path}")
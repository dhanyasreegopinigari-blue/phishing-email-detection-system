import joblib
import traceback

try:
    print('Trying to load phishing_email_model.pkl')
    joblib.load('phishing_email_model.pkl')
    print('Model loaded')
    print('Trying to load vectorizer.pkl')
    joblib.load('vectorizer.pkl')
    print('Vectorizer loaded')
    print('OK')
except Exception:
    traceback.print_exc()

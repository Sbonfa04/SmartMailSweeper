from gmail_auth import get_gmail_service
import base64
import email
import pickle
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords

# Inizializza nltk
nltk.download('stopwords')
stop_words = set(stopwords.words('italian'))

# Carica modello e vettorizzatore
with open("model.pkl", "rb") as f:
    clf = pickle.load(f)
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Pulizia testo
def preprocess(text):
    text = text.lower()
    text = ''.join([c for c in text if c not in string.punctuation])
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return ' '.join(words)

# Estrai corpo email
def clean_payload(payload):
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    return base64.urlsafe_b64decode(data).decode(errors='ignore')
    else:
        data = payload['body'].get('data')
        if data:
            return base64.urlsafe_b64decode(data).decode(errors='ignore')
    return ""

# Classifica e pulisci
def classify_and_clean_emails():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', maxResults=20).execute()
    messages = results.get('messages', [])

    for msg in messages:
        full_msg = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = full_msg['payload']
        headers = payload['headers']

        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        from_ = next((h['value'] for h in headers if h['name'] == 'From'), '')
        body = clean_payload(payload)

        combined_text = preprocess(subject + " " + body)
        vect = vectorizer.transform([combined_text])
        prediction = clf.predict(vect)[0]

        print(f"\nFrom: {from_}\nSubject: {subject}\nPrediction: {prediction}")

        if prediction == "inutile":
            # Puoi scegliere una delle seguenti azioni:
            
            # 1. Archivia (rimuove da inbox)
            service.users().messages().modify(
                userId='me',
                id=msg['id'],
                body={'removeLabelIds': ['INBOX']}
            ).execute()
            print("➡️ Archiviata")

            # 2. Oppure cancella (decommenta se preferisci)
            # service.users().messages().delete(userId='me', id=msg['id']).execute()
            # print("🗑️ Eliminata")

if __name__ == "__main__":
    classify_and_clean_emails()

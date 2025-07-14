from gmail_auth import get_gmail_service
import base64
import email
import pickle
import string
import nltk
import requests

nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words('italian'))

# ====== CONFIGURA QUI ======
BOT_TOKEN = "XXXXXXXXXXX"  # Il tuo token del bot Telegram
YOUR_CHAT_ID = XXXXXXXXX  # tuo user ID telegram
# ===========================

# Carica modello e vettorizzatore
with open("model.pkl", "rb") as f:
    clf = pickle.load(f)
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

def preprocess(text):
    text = text.lower()
    text = ''.join([c for c in text if c not in string.punctuation])
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return ' '.join(words)

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

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": YOUR_CHAT_ID,
        "text": text[:4096]  # Telegram ha limite di 4096 caratteri
    }
    requests.post(url, json=payload)

def notify_useful_emails():
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

        combined = preprocess(subject + " " + body)
        vect = vectorizer.transform([combined])
        pred = clf.predict(vect)[0]

        if pred == "utile":
            text = f"📬 *Nuova mail utile!*\nFrom: {from_}\nSubject: {subject}"
            send_telegram_message(text)

if __name__ == "__main__":
    notify_useful_emails()

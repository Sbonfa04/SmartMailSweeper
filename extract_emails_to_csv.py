from gmail_auth import get_gmail_service
import base64
import email
import pandas as pd
from tqdm import tqdm

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

def main():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', maxResults=200).execute() # è possibile cambiare il numero per estrarre più email in maxResults
    messages = results.get('messages', [])

    data = []

    print("Estrazione in corso...")
    for msg in tqdm(messages):
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = txt['payload']
        headers = payload['headers']
        
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        from_ = next((h['value'] for h in headers if h['name'] == 'From'), '')
        body = clean_payload(payload)

        data.append({
            'from': from_,
            'subject': subject,
            'body': body,
            'label': ''  # Da compilare manualmente in caso si voglia classificare
        })

    df = pd.DataFrame(data)
    df.to_csv("emails_dataset.csv", index=False)
    print("✅ File creato: emails_dataset.csv")

if __name__ == "__main__":
    main()

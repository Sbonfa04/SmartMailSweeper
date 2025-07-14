from gmail_auth import get_gmail_service
import base64
import email

service = get_gmail_service()
results = service.users().messages().list(userId='me', maxResults=5).execute()
messages = results.get('messages', [])

for msg in messages:
    txt = service.users().messages().get(userId='me', id=msg['id']).execute()
    payload = txt['payload']
    headers = payload['headers']
    
    subject = [h['value'] for h in headers if h['name'] == 'Subject']
    from_ = [h['value'] for h in headers if h['name'] == 'From']
    
    print("From:", from_[0] if from_ else "Unknown")
    print("Subject:", subject[0] if subject else "No Subject")
    print("-----------")

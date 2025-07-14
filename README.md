# 📬 SmartMailSweeper

SmartMailSweeper è uno script Python che usa **Machine Learning** e l’**API ufficiale di Gmail** per classificare automaticamente le tue email in **utili** o **inutili**, e **archiviare quelle inutili**.  
In più, ti può notificare su Telegram quando ricevi una nuova email importante!

---

## Funzionalità

- Classificazione automatica delle email usando ML personalizzato
- Archiviazione automatica delle email inutili
- Notifiche Telegram per le email utili
- Automazione giornaliera via `crontab`

---

## Come iniziare

### 1. Crea un progetto Gmail

1. Vai su [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuovo progetto
3. Abilita l’**API Gmail**
4. Crea credenziali **OAuth 2.0** per app desktop
5. Scarica il file `client_secret_XXXXXXXXXXX.json` e mettilo nella root del progetto

---

### 2. 🧱 Installa le dipendenze

Assicurati di usare Python 3.7+ e installa i pacchetti necessari:

```bash
pip install -r requirements.txt
```

Se non hai il file `requirements.txt`, puoi generarlo così:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib python-telegram-bot nltk scikit-learn
pip freeze > requirements.txt
```

### 3. Autenticati con Gmail

All'interno del file `gmail_auth.py` cambia 'client_secret_XXXXXXXXXXX.json' col nome esatto del file scaricato precedentemente.

Lancia una prima volta lo script `read_emails.py`:

```bash
python read_emails.py
```

Verrà aperta una finestra del browser: autorizza l'app con il tuo account Gmail.
Verrà creato un file `token.json` per salvare il login.

In caso di errore in questa fase vai su https://console.cloud.google.com/apis/credentials/consent, nella pagina `Schermata di consenso OAuth`, controlla che sia impostata su:
- Tipo utente: Esterno
- Stato: In test

Scorri fino alla sezione finale della pagina dove troverai `Utenti di test`:
- Clicca su “Aggiungi utenti”
- Inserisci il tuo indirizzo Gmail
- Premi “Salva”

Quando rilanci il tuo script `read_emails.py`, la schermata `l'app non è verificata` ti darà accesso completo cliccando su:

Avanzate → Vai a [Nome app] (non sicuro)

### 4. Etichetta manualmente le email
In caso ti mancassero, installa queste librerie in aggiunta:
```bash
pip install pandas tqdm
```
Ora usa lo script `extract_mail_to_csv.py` per vedere le ultime email e assegnare manualmente nel `CSV` creato le etichette (`utile` o `inutile`).
Questo serve per creare un dataset personalizzato per l’addestramento.

```bash
python extract_mail_to_csv.py
```
Dopo aver assegnato almeno 50-100 etichette, verrà generato un file `emails_dataset.csv`.

### 5. Addestra il classificatore
In caso ti mancassero, installa queste librerie in aggiunta:
```bash
pip install pandas scikit-learn nltk
```
Lancia:
```bash
python train_classifier.py
```
Questo crea un modello salvato in `model.pkl` e un vettorizzatore in `vectorizer.pkl`.

### 6. Classifica e archivia le email
Lancia il classificatore:
```bash
python classify_and_clean.py
```
Questo script legge le ultime email, le classifica e archivia automaticamente quelle marcate come "inutile".
In caso si vuole che le email "inutile" vengano cancellate, aprire `classify_and_clean.py` e modificare la parte finale commentata.

### 7. Ricevi notifiche Telegram (opzionale)

1. Crea un bot con `@BotFather` su Telegram
2. Ottieni il `BOT_TOKEN` e il tuo Telegram ID (utilizza `@userinfobot`)
3. Inseriscili nello script `notify_useful_emails.py`

Poi esegui:
```bash
python notify_useful_emails.py
```
Riceverai le email utili come messaggio Telegram

### 8. Automatizza con crontab (macOS/Linux)
Puoi usare gli script `setup_cron_notify.sh` e `setup_cron_clean.sh` per automatizzare tutto:
```bash
chmod +x setup_cron_clean.sh
./setup_cron_clean.sh
chmod +x setup_cron_notify.sh
./setup_cron_notify.sh
```
Questo imposterà il sistema per classificare e pulire automaticamente ogni giorno alle 9:10.

## Struttura del progetto
```bash
SmartMailSweeper/
├── gmail_auth.py                # Login Gmail + token
├── label_emails.py              # Script per etichettare email
├── train_classifier.py          # Addestra il modello ML
├── classify_and_clean.py        # Classifica e archivia
├── notify_useful_emails.py      # Notifica email utili via Telegram
├── setup_cron_clean.sh          # Automazione cron giornaliera
├── model.pkl / vectorizer.pkl   # Modello e vettorizzatore ML
├── emails_dataset.csv           # Dataset etichettato manualmente
├── cron_clean_log.txt           # Log dell'automazione
├── requirements.txt             # Dipendenze Python
└── README.md
```
## Licenza
Questo progetto è distribuito con licenza MIT, sentiti libero di usarlo, modificarlo e migliorarlo.

## Autore
Creato da Samuele Bonfanti.
In caso di errori o problemi non esitare a contattarmi.
Se ti è utile, lasciami una ⭐ su [GitHub](https://github.com/Sbonfa04) o contattami su [LinkedIn](https://www.linkedin.com/in/samuele-bonfanti-a568042b1/).

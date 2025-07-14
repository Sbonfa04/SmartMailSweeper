#!/bin/bash

# === CONFIGURAZIONE ===

PYTHON_PATH="/opt/homebrew/bin/python3" # Percorso del tuo interprete Python, assicurati che sia corretto
SCRIPT_PATH="/Users/sbonfa/Desktop/SmartMailSweeper/notify_useful_emails.py" # Percorso completo dello script Python da eseguire
LOG_PATH="/Users/sbonfa/Desktop/SmartMailSweeper/cron_log.txt" # Percorso del file di log dove verranno registrati gli output
CRON_EXPR="0 9 * * * $PYTHON_PATH $SCRIPT_PATH >> $LOG_PATH 2>&1" # Esegui ogni giorno alle 9:00 del mattino, in caso di modifiche, aggiorna il percorso del file python e lo script

# ======================

echo "🔍 Controllo cron esistente..."

# Verifica se la riga è già presente
crontab -l 2>/dev/null | grep -F "$SCRIPT_PATH" > /dev/null

if [ $? -eq 0 ]; then
  echo "✅ Cron già presente. Nessuna modifica necessaria."
else
  echo "🛠️  Aggiungo cron al file..."

  (crontab -l 2>/dev/null; echo "$CRON_EXPR") | crontab -

  echo "✅ Cron aggiunto:"
  echo "$CRON_EXPR"
fi

echo "🎯 Fatto! Controlla con: crontab -l"

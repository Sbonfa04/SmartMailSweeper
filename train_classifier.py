import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
import nltk
import string

# Inizializza nltk (stopwords solo al primo avvio)
nltk.download('stopwords')
from nltk.corpus import stopwords

# 🔧 Funzione per pulire il testo
def preprocess(text):
    text = text.lower()
    text = ''.join([c for c in text if c not in string.punctuation])
    words = text.split()
    words = [w for w in words if w not in stopwords.words('italian')]
    return ' '.join(words)

# Carica il dataset
df = pd.read_csv("emails_dataset.csv")

# Debug: mostra info sul dataset
print(f"📊 Dataset caricato: {df.shape[0]} righe, {df.shape[1]} colonne")
print(f"🏷️  Etichette originali: {df['label'].value_counts()}")
print(f"❌ Righe senza etichetta: {df['label'].isnull().sum()}")

# Pulisci le etichette rimuovendo spazi in eccesso
df['label'] = df['label'].str.strip()

# Rimuovi righe con etichette nulle o vuote
df = df.dropna(subset=['label'])
df = df[df['label'] != '']

print(f"\n🧹 Dopo pulizia etichette: {df['label'].value_counts()}")

# Combina oggetto + corpo
df["text"] = df["subject"].fillna('') + " " + df["body"].fillna('')
df["text"] = df["text"].apply(preprocess)

# Rimuovi righe non etichettate (ora con etichette pulite)
df = df[df["label"].isin(["utile", "inutile"])]

print(f"\n✅ Dataset finale: {df.shape[0]} righe")
print(f"📈 Distribuzione finale: {df['label'].value_counts()}")

# Verifica che ci siano abbastanza dati
if len(df) < 10:
    print("\n⚠️  ATTENZIONE: Troppi pochi dati per il training!")
    print("   Servono almeno 10 email etichettate per un training efficace.")
    print("   Considera di etichettare più email nel dataset.")
    exit(1)

# Verifica che ci siano abbastanza esempi per ogni classe
class_counts = df['label'].value_counts()
min_samples_per_class = class_counts.min()
if min_samples_per_class < 3:
    print(f"\n⚠️  ATTENZIONE: Troppi pochi esempi per la classe con meno campioni ({min_samples_per_class})!")
    print("   Servono almeno 3 esempi per ogni classe (utile/inutile) per il training.")
    print("   Distribuzione attuale:")
    for label, count in class_counts.items():
        print(f"     - {label}: {count} esempi")
    exit(1)

# Prepara dati per ML
X = df["text"]
y = df["label"]

print(f"\n🔀 Dividendo dataset in train/test...")
print(f"   Totale esempi: {len(X)}")

# Divisione train/test con stratificazione per mantenere la proporzione delle classi
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42, 
    stratify=y  # Mantiene la proporzione delle classi
)

print(f"   Training set: {len(X_train)} esempi")
print(f"   Test set: {len(X_test)} esempi")

# TF-IDF vettorizzazione
vectorizer = TfidfVectorizer()
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# Classificatore Naive Bayes
clf = MultinomialNB()
clf.fit(X_train_vect, y_train)

# Valutazione
y_pred = clf.predict(X_test_vect)
print("✅ Report valutazione modello:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Salva modello e vettorizzatore
import pickle
with open("model.pkl", "wb") as f:
    pickle.dump(clf, f)
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

for true, pred, text in zip(y_test, y_pred, X_test):
    if true != pred:
        print(f"\n❌ Predetto: {pred} — Reale: {true}\nTesto: {text[:200]}...")


print("Distribuzione etichette:")
print(df["label"].value_counts())
print("Numero righe totali:", len(df))
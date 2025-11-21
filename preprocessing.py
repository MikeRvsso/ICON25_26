import pandas as pd
import shutil
import os
from sklearn.preprocessing import LabelEncoder 

# ==========================================
# 0. CONFIGURAZIONE
# ==========================================
file_path = '../Dataset/amazon_delivery.csv'

# ==========================================
# 1. CARICAMENTO
# ==========================================
try:
    df = pd.read_csv(file_path) 
    print("✅ File caricato!")
except FileNotFoundError:
    print(f"❌ Errore: File non trovato in {file_path}")
    exit()

if 'df' in locals():
    # ==========================================
    # 2. PULIZIA (CLEANING)
    # ==========================================
    # Anche se il file è già pulito, lasciamo queste righe.
    # Se il file è pulito, queste funzioni non faranno nulla (ed è ok!)
    
    print("\n--- FASE DI CLEANING ---")
    righe_start = len(df)

    df = df.drop_duplicates()
    df = df.dropna(subset=['Weather'])
    df = df[df['Agent_Age'] >= 18]
    
    # Rating: ricalcoliamo la mediana e riempiamo (sicuro anche se non ci sono buchi)
    rating_mediano = df['Agent_Rating'].median()
    df['Agent_Rating'] = df['Agent_Rating'].fillna(rating_mediano)
    
    print(f"✅ Pulizia completata (o verificata). Righe attuali: {len(df)}")

    # ==========================================
    # 3. ENCODING (CORRETTO E ROBUSTO)
    # ==========================================
    print("\n--- FASE DI ENCODING ---")

    # 1. PULIZIA PRELIMINARE STRINGHE (Il trucco magico!)
    # .str.strip() rimuove spazi vuoti invisibili all'inizio e alla fine
    # Esempio: " High " diventa "High"
    if df['Traffic'].dtype == 'object':
        df['Traffic'] = df['Traffic'].str.strip()
        # Stampiamo i valori unici per essere sicuri di come sono scritti
        print("Valori reali trovati in Traffic:", df['Traffic'].unique())

    if df['Weather'].dtype == 'object':
        df['Weather'] = df['Weather'].str.strip()

    # 2. ENCODING MANUALE
    # Ora ridefiniamo la mappa (assicurati che i nomi stampati sopra combacino!)
    traffic_map = {'Low': 0, 'Medium': 1, 'High': 2, 'Jam': 3}
    
    # Applichiamo la mappa solo se la colonna è ancora testo
    if df['Traffic'].dtype == 'object': 
        df['Traffic_Code'] = df['Traffic'].map(traffic_map)
        print("✅ Traffico convertito.")
    
    # Meteo
    weather_map = {'Sunny': 0, 'Cloudy': 1, 'Windy': 2, 'Fog': 3, 'Stormy': 4, 'Sandstorms': 5}
    if df['Weather'].dtype == 'object':
        df['Weather_Code'] = df['Weather'].map(weather_map)
        print("✅ Meteo convertito.")

    # 3. ENCODING AUTOMATICO (Vehicle & Category)
    le = LabelEncoder()
    
    if df['Vehicle'].dtype == 'object':
        df['Vehicle_Code'] = le.fit_transform(df['Vehicle'])
        print("✅ Veicolo convertito.")
        
    if df['Category'].dtype == 'object':
        df['Category_Code'] = le.fit_transform(df['Category'])
        print("✅ Categoria convertita.")
        
    # ==========================================
    # 4. SALVATAGGIO
    # ==========================================
    print("\n--- SALVATAGGIO ---")
    
    # Backup di sicurezza (sovrascrive il vecchio backup se c'è)
    backup_path = file_path.replace('.csv', '_OLD.csv')
    shutil.copy(file_path, backup_path)
    print(f"📦 Backup aggiornato: {backup_path}")

    # Sovrascrivi il file originale con le nuove colonne _Code
    df.to_csv(file_path, index=False)
    print(f"💾 File '{file_path}' aggiornato con successo!")
    
    # Verifica finale
    print("\nAnteprima nuove colonne:")
    cols_to_check = [c for c in df.columns if 'Code' in c]
    if cols_to_check:
        print(df[cols_to_check].head(3))
    else:
        print("⚠️ Nessuna colonna '_Code' trovata. Qualcosa non va.")
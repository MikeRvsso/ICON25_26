import pandas as pd
import shutil # Libreria standard per copiare i file (serve per il backup)
import os

# ==========================================
# 0. CONFIGURAZIONE PERCORSO
# ==========================================
# Definiamo il percorso qui, così lo usiamo ovunque
file_path = '../Dataset/amazon_delivery.csv'

# ==========================================
# 1. CARICAMENTO DEL DATASET
# ==========================================
try:
    df = pd.read_csv(file_path) 
    print("✅ File CSV caricato con successo!")
    
except FileNotFoundError:
    print(f"❌ Errore: File non trovato al percorso: {file_path}")
    # df = pd.DataFrame() 

# ==========================================
# 2. ANALISI E PULIZIA
# ==========================================

if 'df' in locals(): # Esegue solo se il file è stato caricato
    
    print("\n" + "="*40)
    print("REPORT DI ANALISI DEL DATASET")
    print("="*40 + "\n")

    # --- A. SGUARDO GENERALE ---
    print("--- 1. ANTEPRIMA DATI ---")
    print(df.head()) 
    
    print("\n--- 2. DIMENSIONI ---")
    rows, cols = df.shape
    print(f"Righe: {rows}, Colonne: {cols}")

    # --- B. TIPI DI DATI ---
    print("\n--- 3. INFO E TIPI DI DATI ---")
    df.info() 

    # --- C. VALORI MANCANTI ---
    print("\n--- 4. CONTEGGIO CELLE VUOTE (NaN) ---")
    missing = df.isnull().sum()
    print(missing[missing > 0]) 

    # --- D. DUPLICATI ---
    print("\n--- 5. RIGHE DUPLICATE ---")
    duplicati = df.duplicated().sum()
    print(f"Righe identiche trovate: {duplicati}")

    # --- E. STATISTICHE RAPIDE ---
    print("\n--- 6. STATISTICHE ---")
    print(df.describe())

    # Controllo specifico Weather
    print("--- Valori unici in Weather ---")
    print(df['Weather'].unique())

    # ==========================================
    # FASE DI CLEANING (PULIZIA)
    # ==========================================
    print("\n" + "="*40)
    print("INIZIO PULIZIA DEL DATASET")
    print("="*40 + "\n")

    righe_iniziali = len(df)

    # 1. GESTIONE METEO (WEATHER)
    df = df.dropna(subset=['Weather'])
    print(f"✅ Eliminate righe con Meteo mancante. (Righe attuali: {len(df)})")

    # 2. GESTIONE ETA' (AGENT_AGE)
    df = df[df['Agent_Age'] >= 18]
    print(f"✅ Eliminati fattorini minorenni (<18). (Righe attuali: {len(df)})")

    # 3. GESTIONE RATING (AGENT_RATING)
    rating_mediano = df['Agent_Rating'].median()
    df['Agent_Rating'] = df['Agent_Rating'].fillna(rating_mediano)
    print(f"✅ Riempiti i Rating mancanti con la mediana ({rating_mediano}).")

    # ==========================================
    # VERIFICA FINALE
    # ==========================================
    print("\n" + "="*40)
    print("VERIFICA POST-PULIZIA")
    print("="*40 + "\n")

    print("Buchi rimasti (dovrebbero essere tutti 0):")
    print(df.isnull().sum())

    print(f"\nTotale righe eliminate: {righe_iniziali - len(df)}")

    # Reset dell'indice
    df = df.reset_index(drop=True)

    # ==========================================
    # 3. SALVATAGGIO (SOVRASCRITTURA SICURA)
    # ==========================================
    print("\n" + "="*40)
    print("SALVATAGGIO FILE")
    print("="*40 + "\n")

    # A. CREAZIONE BACKUP (Non si sa mai!)
    # Creiamo un nome per il backup es: amazon_delivery_OLD.csv
    backup_path = file_path.replace('.csv', '_OLD.csv')
    
    try:
        shutil.copy(file_path, backup_path)
        print(f"📦 Backup di sicurezza creato: {backup_path}")
        
        # B. SOVRASCRITTURA DEL FILE ORIGINALE
        # index=False serve a non aggiungere la colonna dei numeri di riga
        df.to_csv(file_path, index=False)
        print(f"💾 File originale '{file_path}' sovrascritto con i dati puliti!")
        
    except Exception as e:
        print(f"❌ Errore durante il salvataggio: {e}")

else:
    print("Il DataFrame 'df' non è stato creato. Verifica il caricamento del file.")
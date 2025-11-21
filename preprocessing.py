import pandas as pd

# ==========================================
# 1. CARICAMENTO DEL DATASET
# ==========================================
# Sostituisci 'nome_del_tuo_file.csv' con il nome reale del tuo file.

# SE E' UN CSV (più comune):
# A volte i CSV usano il punto e virgola ';' invece della virgola ','
# Se ti dà errore, prova: pd.read_csv('...', sep=';')
try:
    df = pd.read_csv('../Dataset/amazon_delivery.csv') 
    print("✅ File CSV caricato con successo!")
    
except FileNotFoundError:
    print("❌ Errore: File non trovato. Controlla il nome o il percorso.")
    # Se non hai il file pronto, de-commenta la riga sotto per creare un dataframe vuoto di prova
    # df = pd.DataFrame() 

# SE E' UN EXCEL (togli il commento '#' sotto se usi excel):
# df = pd.read_excel('nome_del_tuo_file.xlsx')


# ==========================================
# 2. ANALISI AUTOMATICA (CHECK-UP)
# ==========================================

if 'df' in locals(): # Esegue solo se il file è stato caricato
    
    print("\n" + "="*40)
    print("REPORT DI ANALISI DEL DATASET")
    print("="*40 + "\n")

    # --- A. SGUARDO GENERALE ---
    print("--- 1. ANTEPRIMA DATI ---")
    print(df.head()) # Mostra le prime 5 righe
    
    print("\n--- 2. DIMENSIONI ---")
    rows, cols = df.shape
    print(f"Righe: {rows}")
    print(f"Colonne: {cols}")

    # --- B. TIPI DI DATI ---
    print("\n--- 3. INFO E TIPI DI DATI ---")
    # Fondamentale per vedere se i numeri sono letti come testo (Object)
    df.info() 

    # --- C. VALORI MANCANTI ---
    print("\n--- 4. CONTEGGIO CELLE VUOTE (NaN) ---")
    missing = df.isnull().sum()
    # Filtriamo per mostrare solo le colonne che hanno effettivamente buchi
    print(missing[missing > 0]) 

    # --- D. DUPLICATI ---
    print("\n--- 5. RIGHE DUPLICATE ---")
    duplicati = df.duplicated().sum()
    print(f"Righe identiche trovate: {duplicati}")

    # --- E. STATISTICHE RAPIDE ---
    print("\n--- 6. STATISTICHE (Solo colonne numeriche) ---")
    # Utile per beccare al volo numeri strani (es. Prezzo massimo altissimo)
    print(df.describe())


    # Mostra i valori unici presenti nella colonna Weather
    print("--- Valori unici in Weather ---")
    print(df['Weather'].unique())

    # Filtriamo e stampiamo alcune delle righe dove Weather è vuoto
    print("\n--- Esempio di righe con Weather mancante ---")
    missing_weather = df[df['Weather'].isnull()]
    print(missing_weather.head(5))

    # ==========================================
    # FASE DI CLEANING (PULIZIA)
    # ==========================================
    print("\n" + "="*40)
    print("INIZIO PULIZIA DEL DATASET")
    print("="*40 + "\n")

    # Salvo il numero di righe iniziali per vedere quante ne togliamo
    righe_iniziali = len(df)

    # 1. GESTIONE METEO (WEATHER)
    # Eliminiamo le righe dove Weather è NaN (Not a Number)
    # subset=['Weather'] dice di controllare solo quella colonna
    df = df.dropna(subset=['Weather'])
    print(f"✅ Eliminate righe con Meteo mancante. (Righe attuali: {len(df)})")

    # 2. GESTIONE ETA' (AGENT_AGE)
    # Teniamo solo chi ha almeno 18 anni.
    # Filtriamo via i 15enni (probabili errori di sistema)
    df = df[df['Agent_Age'] >= 18]
    print(f"✅ Eliminati fattorini minorenni (<18). (Righe attuali: {len(df)})")

    # 3. GESTIONE RATING (AGENT_RATING)
    # Qui invece di cancellare, riempiamo i buchi.
    # Calcoliamo la mediana (valore centrale, più robusto della media contro gli outlier)
    rating_mediano = df['Agent_Rating'].median()
    print(f"ℹ️ Il Rating mediano calcolato è: {rating_mediano}")

    # Riempiamo i NaN nella colonna Rating con questo valore
    df['Agent_Rating'] = df['Agent_Rating'].fillna(rating_mediano)
    print("✅ Riempiti i Rating mancanti con la mediana.")

    # ==========================================
    # VERIFICA FINALE
    # ==========================================
    print("\n" + "="*40)
    print("VERIFICA POST-PULIZIA")
    print("="*40 + "\n")

    # Controlliamo se ci sono ancora buchi
    print("Buchi rimasti (dovrebbero essere tutti 0):")
    print(df.isnull().sum())

    print(f"\nTotale righe eliminate: {righe_iniziali - len(df)}")

    # Reset dell'indice (per avere i numeri di riga ordinati 0,1,2... dopo i tagli)
    df = df.reset_index(drop=True)

else:
    print("Il DataFrame 'df' non è stato creato. Verifica il caricamento del file.")
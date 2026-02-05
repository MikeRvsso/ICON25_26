import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Imposta lo stile globale
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'serif' 
plt.rcParams['figure.dpi'] = 300 

def generate_graphs():
    # Carica il dataset
    # Determina il percorso del file CSV relativo allo script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'amazon_delivery_optimized.csv')
    
    try:
        df = pd.read_csv(csv_path)
        print(f"Dataset caricato con successo da {csv_path}.")
    except FileNotFoundError:
        print(f"Errore: File '{csv_path}' non trovato.")
        return

    # --- GRAFICO 1: Mappa di Zonizzazione (Scatter Plot Geografico) ---
    print("Generazione Grafico 1: Mappa di Zonizzazione...")
    
    plt.figure(figsize=(10, 8))
    
    # Rimuovi eventuali righe con NaN nelle coordinate o Van_ID se necessario
    df_geo = df.dropna(subset=['Drop_Latitude', 'Drop_Longitude', 'Van_ID'])
    
    # Ottieni i Van_ID unici
    unique_vans = sorted(df_geo['Van_ID'].unique())
    palette = sns.color_palette("viridis", len(unique_vans))
    
    # Scatter plot dei punti consegna
    sns.scatterplot(
        data=df_geo, 
        x='Drop_Longitude', 
        y='Drop_Latitude', 
        hue='Van_ID', 
        palette=palette,
        s=30, 
        alpha=0.6,
        edgecolor=None
    )
    
    # Calcolo dei centroidi
    centroids = df_geo.groupby('Van_ID')[['Drop_Latitude', 'Drop_Longitude']].mean()
    
    # Plot dei centroidi
    plt.scatter(
        centroids['Drop_Longitude'], 
        centroids['Drop_Latitude'], 
        s=200, 
        marker='*', 
        color='red', 
        edgecolor='white', 
        linewidth=1,
        label='Centroidi', 
        zorder=10
    )
    
    plt.title('Zonizzazione Territoriale', fontsize=16, fontweight='bold', pad=15)
    plt.xlabel('Longitudine', fontsize=12)
    plt.ylabel('Latitudine', fontsize=12)
    plt.legend(title='ID Furgone', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig('zonizzazione_territoriale.png')
    plt.close()
    print("Grafico 1 salvato come 'zonizzazione_territoriale.png'.")

    # --- GRAFICO 2: Analisi del Carico (Bin Packing) ---
    print("Generazione Grafico 2: Analisi del Carico...")
    
    # Filtra solo i pacchi caricati
    df_loaded = df[df['Status'] == 'Loaded'].copy()
    
    if df_loaded.empty:
        print("Attenzione: Nessun pacco con stato 'Loaded' trovato. Verificare il dataset.")
        # Se vuoto, provo a usare tutto il dataset raggruppato per Van_ID assumendo che Van_ID > -1 siano assegnati
        # Questo è un fallback nel caso i dati non abbiano 'Loaded' esplicito ma abbiano Van_ID assegnati
        df_loaded = df[df['Van_ID'] != -1].copy() # Assumiamo -1 sia non assegnato/skipped se 'Loaded' non c'è
        print(f"Fallback: Usati {len(df_loaded)} pacchi con Van_ID assegnato.")

    # Conta pacchi per furgone
    load_counts = df_loaded['Van_ID'].value_counts().sort_index()
    
    # Prepara dati per il grafico
    van_ids = load_counts.index
    loaded_vals = load_counts.values
    capacity = 50
    free_space = capacity - loaded_vals
    # Assicuriamoci che non sia negativo (se sovraccarico)
    free_space = np.maximum(free_space, 0) 
    
    plt.figure(figsize=(12, 6))
    
    indices = np.arange(len(van_ids))
    width = 0.6
    
    # Barra caricata (Parte bassa)
    plt.bar(indices, loaded_vals, width, label='Carico Attuale', color='#3498db', alpha=0.9, zorder=3)
    
    # Barra spazio libero (Parte alta)
    plt.bar(indices, free_space, width, bottom=loaded_vals, label='Spazio Libero', 
            color='#ecf0f1', edgecolor='#bdc3c7', hatch='//', alpha=0.6, zorder=3)
    
    # Linea soglia critica (90% di 50 = 45)
    threshold = 0.9 * capacity
    plt.axhline(y=threshold, color='red', linestyle='--', linewidth=2, label='Soglia Critica (90%)', zorder=4)
    
    # Etichette
    for i, v in enumerate(loaded_vals):
        color = 'black'
        fontweight = 'normal'
        if v >= threshold:
            color = '#c0392b'
            fontweight = 'bold'
        
        # Posiziona etichetta leggermente sopra la parte caricata o dentro se c'è spazio
        pos_y = v + 1 if v < capacity else v + 1
        plt.text(i, pos_y, str(v), ha='center', va='bottom', fontsize=11, fontweight=fontweight, color=color)
        
    plt.title('Analisi del Carico Furgoni (Bin Packing)', fontsize=16, fontweight='bold', pad=15)
    plt.xlabel('ID Furgone', fontsize=12)
    plt.ylabel('Numero di Pacchi', fontsize=12)
    plt.xticks(indices, [f'Van {vid}' for vid in van_ids], rotation=45)
    plt.ylim(0, capacity + 5) # Un po' di margine sopra
    plt.legend(loc='upper right')
    plt.grid(axis='x') # Rimuovi griglia verticale per pulizia
    
    plt.tight_layout()
    plt.savefig('analisi_carico_furgoni.png')
    plt.close()
    print("Grafico 2 salvato come 'analisi_carico_furgoni.png'.")

if __name__ == "__main__":
    generate_graphs()

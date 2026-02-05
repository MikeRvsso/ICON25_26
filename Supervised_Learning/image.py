import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import warnings

# Ignora warning di sklearn se ci sono versioni diverse
warnings.filterwarnings("ignore")

def load_data_and_split():
    """Carica il dataset e prepara X_train, X_test, y_train, y_test come nel notebook."""
    try:
        # Costruisci il percorso in modo relativo alla posizione dello script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir, '../Preprocessing', 'amazon_delivery_final.csv')
        
        print(f"Caricamento dati da: {data_path}")
        df = pd.read_csv(data_path)
        
        # Preprocessing base (come in ml_modulo.ipynb)
        if 'Order_ID' in df.columns:
            df = df.drop(columns=['Order_ID'])
            
        target_column = 'Delivery_Time'
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Split identico al training (random_state=42)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=42
        )
        return X_train, X_test, y_train, y_test, X.columns
    except Exception as e:
        print(f"Errore nel caricamento dati: {e}")
        return None, None, None, None, None

def load_models(script_dir):
    """Carica i modelli salvati nella cartella corrente."""
    models = {}
    model_files = {
        'Linear Regression': 'linear_model.pkl',
        'Decision Tree': 'decision_tree_model.pkl',
        'Random Forest': 'delivery_model.pkl', # Assumiamo che delivery_model sia il RF principale
        'XGBoost': 'xgboost_model.pkl'
    }
    
    for name, filename in model_files.items():
        path = os.path.join(script_dir, filename)
        if os.path.exists(path):
            try:
                models[name] = joblib.load(path)
                print(f"Modello caricato: {name}")
            except Exception as e:
                print(f"Impossibile caricare {name}: {e}")
        else:
            print(f"File modello non trovato: {filename}")
            
    return models

# 1. Grafico Feature Importance (Solo Random Forest o XGBoost)
def plot_feature_importance(model, feature_names, save_dir):
    if not hasattr(model, 'feature_importances_'):
        print("Il modello non supporta feature_importances_")
        return

    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    # Prendiamo solo le top 15 per leggibilità
    top_n = 15
    indices = indices[:top_n]
    
    plt.figure(figsize=(12, 8))
    plt.title("Figura 2.x: Top 15 Feature Importance (Random Forest)", fontsize=14)
    plt.barh(range(len(indices)), importances[indices], align="center", color='skyblue')
    plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
    plt.xlabel("Importanza Relativa")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    output_path = os.path.join(save_dir, 'feature_importance.png')
    plt.savefig(output_path, dpi=300)
    print(f"Grafico salvato: {output_path}")
    plt.close()

# 2. Grafico Predetto vs Reale
def plot_predicted_vs_actual(y_test, y_pred, save_dir, model_name="Random Forest"):
    plt.figure(figsize=(8, 8))
    
    # Campionamento per non appesantire il grafico se ci sono troppi punti
    if len(y_test) > 2000:
        indices = np.random.choice(len(y_test), 2000, replace=False)
        y_test_plot = y_test.iloc[indices] if isinstance(y_test, pd.Series) else y_test[indices]
        y_pred_plot = y_pred[indices]
    else:
        y_test_plot = y_test
        y_pred_plot = y_pred

    plt.scatter(y_test_plot, y_pred_plot, alpha=0.3, edgecolors='w', linewidth=0.5)
    
    # Linea diagonale perfetta
    min_val = min(y_test_plot.min(), y_pred_plot.min())
    max_val = max(y_test_plot.max(), y_pred_plot.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Predizione Perfetta')
    
    plt.title(f"Predetto vs Reale ({model_name})", fontsize=14)
    plt.xlabel("Valore Reale (Delivery Time Standardizzato)")
    plt.ylabel("Valore Predetto")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = os.path.join(save_dir, 'predicted_vs_actual.png')
    plt.savefig(output_path, dpi=300)
    print(f"Grafico salvato: {output_path}")
    plt.close()

# 3. Confronto Modelli
def plot_model_comparison(models, X_test, y_test, save_dir):
    metrics_data = {'Modello': [], 'R2': [], 'RMSE': []}
    
    for name, model in models.items():
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        metrics_data['Modello'].append(name)
        metrics_data['R2'].append(r2)
        metrics_data['RMSE'].append(rmse)
        
    df_metrics = pd.DataFrame(metrics_data)
    
    # Plotting
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Posizioni barre
    x = np.arange(len(df_metrics))
    width = 0.35
    
    rects1 = ax1.bar(x - width/2, df_metrics['R2'], width, label='R2 Score', color='tab:blue')
    ax1.set_ylabel('R2 Score', color='tab:blue', fontsize=12)
    ax1.set_title('Confronto Performance Modelli', fontsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_metrics['Modello'])
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.set_ylim(0, 1.1)  # R2 è max 1
    
    ax2 = ax1.twinx()
    rects2 = ax2.bar(x + width/2, df_metrics['RMSE'], width, label='RMSE', color='tab:orange')
    ax2.set_ylabel('RMSE (Errore Quadratico Medio)', color='tab:orange', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='tab:orange')
    
    # Aggiungi etichette valori sopra le barre
    def autolabel(rects, ax):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)

    autolabel(rects1, ax1)
    autolabel(rects2, ax2)
    
    fig.legend(loc="upper right", bbox_to_anchor=(0.85, 0.88))
    plt.tight_layout()

    output_path = os.path.join(save_dir, 'model_comparison.png')
    plt.savefig(output_path, dpi=300)
    print(f"Grafico salvato: {output_path}")
    plt.close()

if __name__ == "__main__":
    # Setup
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, 'images')
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        print(f"Creata cartella immagini: {images_dir}")
    
    # 1. Carica Dati
    X_train, X_test, y_train, y_test, feature_names = load_data_and_split()
    
    if X_test is not None:
        # 2. Carica Modelli
        loaded_models = load_models(script_dir)
        
        if loaded_models:
            print("\n--- Generazione Grafici e Salvataggio ---\n")
            
            # Grafico 1: Feature Importance (Usa Random Forest se c'è, altrimenti primo disponibile con feature_importances_)
            rf_model = loaded_models.get('Random Forest')
            if rf_model:
                plot_feature_importance(rf_model, feature_names, images_dir)
            
            # Grafico 2: Predetto vs Reale (Random Forest)
            if rf_model:
                y_pred_rf = rf_model.predict(X_test)
                plot_predicted_vs_actual(y_test, y_pred_rf, images_dir, "Random Forest")
            
            # Grafico 3: Confronto Modelli (Passiamo i dati reali per calcolare le metriche al volo)
            plot_model_comparison(loaded_models, X_test, y_test, images_dir)
            
            print(f"\nTutti i grafici sono stati salvati in: {images_dir}")
        else:
            print("Nessun modello caricato. Esegui prima i notebook di training per generare i file .pkl")

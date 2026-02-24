# Progetto per Ingegneria della Conoscenza(ICON 2025/2026)

Questo repository contiene il progetto per il corso di **Ingegneria della Conoscenza (ICON)**, sviluppato in Python e Prolog. L'obiettivo del progetto è applicare svariate tecniche e algoritmi di Intelligenza Artificiale su un dataset reale riguardante le consegne di Amazon, per analizzare dati, ottimizzare processi decisionali e prevedere tempi e caratteristiche di consegna.

Il progetto è suddiviso in diverse cartelle, ognuna focalizzata su un ambito specifico dell'Intelligenza Artificiale.

## Struttura del Progetto

Di seguito viene illustrata l'architettura logica e la suddivisione del lavoro all'interno del repository:

### 1. Preprocessing (`/Preprocessing`)
In questo modulo viene analizzato, pulito ed esplorato il dataset originale (`amazon_delivery_start.csv`). Le operazioni includono la rimozione di valori anomali, la gestione dei dati mancanti, il bilanciamento delle frequenze, e lo studio di correlazioni statistiche (es. indici di Spearman), per preparare i dati ai passaggi e ai modelli successivi.

### 2. Ricerca (`/Search`)
In questo script (`search.ipynb`) vengono testate e applicate diverse tecniche di **Ricerca nello Spazio degli Stati** (come ricerca non informata e algoritmi di ricerca euristica, quali A* o similari). L'intento principale in genere riguarda la ricerca e l'ottimizzazione del percorso di consegna.

### 3. Constraint Satisfaction Problem (`/Csp`)
Contiene modelli per la risoluzione di problemi di soddisfacimento di vincoli, applicati sui dati di consegna estratti dal dataset (es: `csp_mumbai_espanso.csv`). Si punta a determinare soluzioni valide per l'assegnazione e l'organizzazione delle tratte di consegna.

### 4. Prolog - Sistema Esperto (`/Prolog`)
Sviluppo di un sistema esperto scritto in linguaggio **Prolog** (`sistema_esperto_mumbai.pl`). Tale sistema include regole del dominio per effettuare dell'inferenza logica e suggerire azioni, valutare condizioni di consegna o risolvere problemi operativi specifici legati alla logistica.

### 5. Reti Bayesiane (`/BayesianNetwork`)
Modellazione dell'incertezza mediante **Reti Bayesiane**. Utilizzando i dati preparati (`dataset_bayes_mumbai.csv`), il modulo consente l'inferenza probabilistica su diversi eventi della rete e la rappresentazione a Grafo Diretto Aciclico (DAG).

### 6. Apprendimento Supervisionato (`/Supervised_Learning`)
Sviluppo, allenamento e validazione di modelli di **Machine Learning**. Vengono creati diversi classificatori e modelli di regressione:
- Alberi di Decisione (`decision_tree_model.pkl`)
- Modelli Lineari (`linear_model.pkl`)
- XGBoost (`xgboost_model.pkl`)

L'obiettivo è creare modelli predittivi ad alte prestazioni (ad esempio, per prevedere le tempistiche o lo status di una consegna).

## Documentazione

Per maggiori dettagli approfonditi sull'implementazione, le metriche valutate teoricamente e la discussione dei risultati ottenuti da ciascun modulo algoritmico, fare riferimento al report completo del progetto allegato all'interno della directory:
* [`Documentazione_Progetto.pdf`](./Documentazione_Progetto.pdf)

## Installazione e Dipendenze

Per replicare l'ambiente di lavoro con i Jupyter Notebook associati ad ogni cartella e i vari file testati in python, si prega di installare le dipendenze contenute all'interno del file testuale dedicato:

```bash
pip install -r requirements.txt
```
Tra le librerie di base si trovano `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn` e l'infrastruttura di lavoro `jupyter`.

## Avviare il Progetto
Data la modularità naturale del lavoro, puoi concentrarti sull'esplorazione del progetto aprendo l'ambiete di sviluppo sul modulo desiderato:
```bash
jupyter notebook
```
Dopodiché, basterà esplorare il file con l'estensione `.ipynb` (es: `preprocessing.ipynb`, `ml_modulo.ipynb` ecc.) della materia di rilievo di cui vuoi eseguire tutti ritorni applicativi.

# Documentazione Modulo Preprocessing

## SEZIONE 1: Sommario

Il modulo analizzato si occupa della fase preliminare di **Data Preprocessing** e **Exploratory Data Analysis (EDA)** per il task di regressione mirato alla stima dei tempi di consegna ("Delivery_Time").
L'**input** del sistema è costituito dal dataset grezzo `amazon_delivery.csv`, contenente lo storico degli ordini con attributi eterogenei quali dati anagrafici dei corrieri, condizioni meteo, traffico, tipologia di veicolo e coordinate geografiche.
L'**output** atteso è un dataset strutturato, pulito e numerico (`amazon_delivery_final.csv`), pronto per l'addestramento di algoritmi di Machine Learning supervisionato.
L'**obiettivo** principale di questo script è trasformare i dati grezzi in feature informative, rimuovendo anomalie e rumore, normalizzando le variabili numeriche e codificando quelle categoriche, al fine di massimizzare l'accuratezza dei modelli predittivi successivi. Inoltre, si ßprefigge di analizzare le relazioni tra le variabili tramite matrici di correlazione per identificare i predittori più significativi del tempo di consegna.

## SEZIONE 2: Strumenti utilizzati

Per l'implementazione della pipeline di preprocessing sono state impiegate le seguenti librerie:

*   **Pandas**: Utilizzata per la manipolazione strutturata dei dati tabulari (DataFrame), la lettura/scrittura di file CSV e le operazioni di filtraggio.
*   **NumPy**: Impiegata per il calcolo numerico efficiente e la gestione delle maschere nelle operazioni matriciali (es. per la heatmap).
*   **Matplotlib / Seaborn**: Adoperate per la generazione di grafici statistici, in particolare per la visualizzazione delle matrici di correlazione (Heatmap).
*   **Scikit-learn (Preprocessing)**: Fondamentale per le trasformazioni dei dati, specificatamente attraverso `StandardScaler` per la standardizzazione delle feature numeriche.

## SEZIONE 3: Decisioni di Progetto

La pipeline di elaborazione dei dati è stata progettata seguendo un approccio sequenziale volto a garantire la qualità e la consistenza del dataset.

### Trattamento dei Dati
La fase di pulizia inizia con la rimozione di colonne ridondanti (codici numerici 'Code' che duplicano informazioni categoriche) e la sanitizzazione delle stringhe tramite trimming. Viene effettuato un filtraggio rigoroso sulle coordinate geografiche, eliminando i record che presentano valori mancanti (coordinate a 0,0) o inconsistenti (latitudini negative), ritenuti errori di rilevazione GPS.

### Trasformazione e Encoding
Per gestire l'eterogeneità delle feature, sono state adottate due strategie distinte:
1.  **Standardizzazione**: Per le variabili numeriche (`Agent_Age`, `Agent_Rating`, `Delivery_Time`), si è scelto l'utilizzo dello `StandardScaler`. Questa tecnica ridimensiona la distribuzione dei valori affinché abbiano media zero e deviazione standard unitaria, prevenendo che variabili con scale maggiori dominino il processo di apprendimento (es. l'età rispetto al rating).
2.  **One-Hot Encoding**: Le variabili categoriche nominali (`Weather`, `Traffic`, `Vehicle`, `Area`, `Category`) sono state trasformate in vettori binari (dummy variables). Questa scelta è preferibile al label encoding per evitare di introdurre un ordinamento fittizio tra le categorie che non presentano una gerarchia intrinseca.

### Analisi delle Correlazioni
La decisione di utilizzare il coefficiente di correlazione di **Spearman** invece di quello di Pearson denota l'intenzione di catturare relazioni monotone non necessariamente lineari tra le variabili, rendendo l'analisi più robusta rispetto a eventuali outlier residui. Infine, le feature temporali (`Pickup_Time`, `Order_Time`) sono state rimosse dal dataset finale, presumibilmente perché il modello target non è progettato per gestire serie temporali o perché l'informazione è stata ritenuta non rilevante dopo l'estrazione delle caratteristiche principali.

## SEZIONE 4: Valutazione

L'efficacia del preprocessing è valutata attraverso report statistici e visualizzazioni grafiche generate automaticamente dal codice.

### Risultati quantitativi
Il sistema produce un file di report dettagliato (`analisi_dataset_2.txt`) che monitora la "salute" del dataset prima e dopo le operazioni. Vengono calcolate metriche descrittive (media, mediana, quartili) ed evidenziati gli outlier tramite il metodo IQR. Il codice esplicita a video il numero di record scartati (es. coordinate nulle), permettendo di valutare l'impatto della pulizia sulla dimensione del campione.

### Analisi delle relazioni
I risultati dell'analisi di correlazione vengono salvati in grafici specifici (`spearman_correlation_target.png`, `full.png`).
L'analisi permette di quantificare l'influenza delle variabili sul target `Delivery_Time`, stampando a terminale le feature con correlazione positiva e negativa più forte. Inoltre, viene effettuato un controllo di multicollinearità, identificando e segnalando le coppie di feature indipendenti che presentano una correlazione assoluta superiore alla soglia di 0.5, fornendo indicazioni utili per un'eventuale successiva feature selection.

# Documentazione Modulo CSP (Vehicle Routing & Optimization)

## --- SEZIONE 1: Sommario ---
Il modulo affronta un problema di **ottimizzazione logistica** combinando tecniche di *Vehicle Routing* e *Bin Packing*. Nello specifico, il sistema deve gestire la pianificazione delle consegne per una flotta di furgoni limitata, partendo da predizioni sui tempi di consegna generate da un modello di Machine Learning.

*   **Input**: Il sistema riceve in ingresso il dataset `amazon_delivery_with_predictions.csv`, contenente le coordinate geografiche di consegna (`Drop_Latitude`, `Drop_Longitude`) e i tempi di consegna predetti standardizzati (`Predicted_Time`).
*   **Output**: Viene generato un file `amazon_delivery_optimized.csv` arricchito con l'assegnazione del furgone (`Van_ID`), il tempo stimato in minuti reali (`Time_Minutes`) e lo stato di accettazione del pacco (`Status` Loaded/Skipped). Vengono inoltre prodotti report in markdown (`csp_report.md`, `fleet_planning_report.md`) per l'analisi manageriale.
*   **Obiettivo**: L'obiettivo primario è massimizzare il numero di consegne effettuate entro il turno lavorativo di 8 ore, rispettando i vincoli di capacità e ottimizzando la distribuzione geografica delle rotte per i 5 furgoni disponibili.

## --- SEZIONE 2: Strumenti utilizzati ---
Di seguito le principali librerie impiegate per l'implementazione della soluzione:

*   **Pandas**: Utilizzata per la manipolazione strutturata dei dati, il caricamento del CSV e la gestione delle trasformazioni tabellari.
*   **Numpy**: Impiegata per operazioni numeriche efficienti e calcoli vettoriali durante la fase di de-standardizzazione.
*   **Scikit-learn (KMeans)**: Algoritmo di clustering non supervisionato utilizzato per la suddivisione territoriale delle consegne basata sulla prossimità geografica.
*   **Math & Datetime**: Librerie standard per calcoli matematici (arrotondamenti per eccesso nel fleet planning) e timestamping dei report.
*   **Sys & IO**: Utilizzate per catturare lo standard output e generare automaticamente report testuali dettagliati.

## --- SEZIONE 3: Decisioni di Progetto ---
L'architettura del software si articola in tre fasi sequenziali distinte, progettate per trasformare dati grezzi in un piano operativo:

### 1. Trattamento dei Dati (De-standardizzazione)
I dati in ingresso presentano tempi di consegna sotto forma di *Z-scores* (standardizzati). Poiché la pianificazione operativa richiede unità temporali reali, è stata implementata una funzione di mapping inverso (`destandardize_time`).
Si applica una trasformazione lineare che rimappa i valori dall'intervallo standardizzato a un range operativo realistico definito tra 10 e 120 minuti (`MIN_DELIVERY_TIME`, `MAX_DELIVERY_TIME`), rendendo i dati utilizzabili per i calcoli di capacità.

### 2. Modellazione del Problema (Clustering Geografico)
Per suddividere il carico di lavoro tra i furgoni, il problema è stato modellato spazialmente utilizzando l'algoritmo **K-Means Clustering**.
*   **Scelta Algoritmica**: K-Means è stato preferito per la sua capacità di minimizzare la varianza intra-cluster, garantendo che ogni furgone operi in una zona geografica compatta.
*   **Configurazione**: Il numero di cluster `k` è stato fissato a 5 (`NUM_VANS`), corrispondente alla dimensione della flotta attuale. Questo assegna implicitamente ogni ordine a una specifica zona operativa (`Van_ID`).

### 3. Algoritmo di Ottimizzazione (Greedy Bin Packing)
L'assegnazione finale dei pacchi al turno lavorativo è gestita come un problema di *Bin Packing* con vincolo di capacità fissa (480 minuti/turno).
*   **Strategia**: È stato implementato un algoritmo **Greedy** con euristica di ordinamento per tempo crescente ("Smallest Items First").
*   **Razionale**: A differenza dell'approccio "Largest Items First" (che massimizza il riempimento del volume), ordinare i pacchi dal più veloce al più lento massimizza il **throughput** (numero totale di consegne effettuate), che è la metrica prioritaria in questo scenario. I pacchi che eccedono la capacità vengono marcati come `Skipped`.

## --- SEZIONE 4: Valutazione ---
Il sistema include un modulo di *Fleet Capacity Planning* che valuta le performance della pianificazione rispetto alla domanda totale.

*   **Metriche di Efficienza**: Il codice calcola la saturazione di ogni furgone e l'efficienza complessiva della flotta. Dai report generati (es. `fleet_planning_report.md`), emerge una forte discrepanza tra capacità attuale e domanda.
*   **Risultati dell'Analisi**:
    *   La simulazione evidenzia un massiccio deficit di risorse: con i soli 5 furgoni disponibili, la copertura della domanda è stimata essere estremamente bassa (nell'ordine dello 0.10% in scenari di alto carico).
    *   Il *Gap Analysis* calcola che per evadere l'intero dataset in un singolo turno sarebbero necessari migliaia di furgoni (teoricamente ~4946 nel report analizzato), o alternativamente circa 989 giorni lavorativi con la flotta attuale.
*   **Output**: Il sistema produce un report dettagliato con raccomandazioni strategiche (Scale-Up, Doppio Turno, Outsourcing) basate sui dati calcolati.

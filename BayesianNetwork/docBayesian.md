# Documentazione Tecnica: Modulo Rete Bayesiana (Bayesian Network)

## 1. Sommario

Il modulo implementa una **Rete Bayesiana (BN)** per l'analisi probabilistica del rischio nelle consegne logistiche. Il problema affrontato è la modellazione delle incertezze e delle dipendenze causali tra i fattori ambientali, umani e operativi che influenzano le prestazioni del servizio.

*   **Input:** Il dataset storico degli ordini (`amazon_delivery_optimized.csv`), contenente metriche quantitative e qualitative quali condizioni meteorologiche, densità del traffico, età del fattorino e tempi di percorrenza effettivi.
*   **Output:** Un modello grafico probabilistico addestrato (rappresentato dalle Tabelle di Probabilità Condizionata - CPT) e set di inferenze statistiche che stimano la probabilità dello stato della consegna ("Puntuale" o "Ritardo") date specifiche evidenze osservate.
*   **Obiettivo:** Quantificazione del rischio e comprensione strutturale del dominio. Il sistema permette di effettuare ragionamenti sia *predittivi* (dalle cause agli effetti) che *diagnostici* (dagli effetti alle cause probabili), superando la mera classificazione binaria.

## 2. Strumenti Utilizzati

Le principali librerie impiegate per lo sviluppo del modulo sono:

*   **Pandas:** Utilizzata per il caricamento, la pulizia dei dati e le operazioni di manipolazione del DataFrame (es. `apply`, `copy`).
*   **Numpy:** Impiegata per il supporto alle operazioni numeriche e la gestione di array multidimensionali.
*   **Pgmpy (Probabilistic Graphical Models in Python):** Libreria fondamentale che fornisce le classi per la definizione della struttura della rete (`DiscreteBayesianNetwork`), gli algoritmi di stima dei parametri (`MaximumLikelihoodEstimator`) e il motore di inferenza esatta (`VariableElimination`).

## 3. Decisioni di Progetto

L'architettura del software si basa su una rigorosa pipeline di trasformazione dei dati e modellazione causale.

### Trattamento dei Dati (Preprocessing e Discretizzazione)
Poiché le Reti Bayesiane discrete operano su spazi di stati finiti, è stata implementata una fase preliminare di discretizzazione delle variabili continue:
*   **Età Autista:** La variabile `Agent_Age` (normalizzata) è stata segmentata in tre fasce categoriche ("Giovane", "Adulto", "Senior") basandosi su soglie statistiche definite (es. valori inferiori a -0.5 deviazioni standard identificano la classe "Giovane").
*   **Variabile Target:** La variabile continua `Time_Minutes` è stata convertita in una variabile binaria di stato `Delivery_Status` ("Puntuale" vs "Ritardo") utilizzando una soglia critica di dominio fissata a 45 minuti.
*   **Ricostruzione Variabili:** Le variabili categoriche relative a Meteo e Traffico, originariamente in formato One-Hot Encoding, sono state ricostruite in singole variabili nominali (`Weather_conditions`, `Road_traffic_density`) per ridurre la complessità topologica del grafo.

### Modellazione del Problema (DAG)
La struttura della rete è definita tramite un Grafo Diretto Aciclico (DAG) progettato su conoscenza esperta (*Expert Knowledge*). La topologia stabilisce esplicitamente le seguenti dipendenze causali:
1.  Il *Meteo* influenza causalmente sia la *Densità del Traffico* che lo *Stato della Consegna*.
2.  Il *Traffico* influenza direttamente lo *Stato della Consegna*.
3.  L'*Esperienza dell'Autista* (Età) agisce come fattore mitigante o aggravante sullo *Stato della Consegna*.

### Scelta Algoritmica
*   **Learning:** Per l'apprendimento dei parametri è stato utilizzato lo stimatore di **Massima Verosimiglianza (MLE - Maximum Likelihood Estimation)**. Questo metodo calcola le probabilità condizionate misurando la frequenza relativa delle co-occorrenze degli stati nel dataset di training, costruendo così le CPT per ogni nodo.
*   **Inference:** Per l'interrogazione della rete, si è optato per l'algoritmo di **Eliminazione di Variabile (Variable Elimination)**. Questo garantisce il calcolo esatto delle probabilità marginali sommando sulle variabili non osservate, risultando preferibile rispetto a metodi approssimati data la dimensione contenuta della rete.

## 4. Valutazione

La validazione del modello è stata condotta attraverso verifiche di consistenza (somma delle probabilità unitaria) e l'analisi di scenari operativi simulati:

*   **Analisi Predittiva (Scenario Pessimistico):** In presenza di evidenze quali "Meteo Tempesta" (`Stormy`), "Traffico congestionato" (`Jam`) e "Autista Giovane", il modello calcola un'elevata probabilità a posteriori per lo stato "Ritardo". Il codice identifica questa combinazione come situazione ad alto rischio, quantificando l'impatto negativo cumulativo dei fattori.
*   **Analisi Predittiva (Scenario Ottimistico):** Configurando le evidenze su condizioni ideali ("Sole", "Traffico Basso", "Autista Senior"), il sistema restituisce una probabilità di puntualità massimizzata, confermando la coerenza logica delle dipendenze apprese.
*   **Analisi Diagnostica:** Mediante inferenza inversa (Backwards Reasoning), osservando un evento di "Ritardo" con un "Autista Esperto", il modello aggiorna le credenze sulla variabile non osservata `Road_traffic_density`, assegnando una probabilità maggiore agli stati di traffico intenso (`High` o `Jam`), fornendo così una spiegazione causale plausibile.
*   **Output:** Il modulo produce stampe dettagliate delle CPT e tabelle comparative delle probabilità per i diversi scenari, salvando infine il dataset processato nel file `bayesian_training_data.csv` per usi futuri.
ß
## 5. Log di Esecuzione

Di seguito viene riportato l'output completo generato dal sistema, che illustra il processo di apprendimento e i risultati delle inferenze.

```text
📈 Distribuzione delle variabili:
--------------------------------------------------

🔹 Weather_conditions:
   Fog: 6784 (17.0%)
   Stormy: 6757 (16.9%)
   Cloudy: 6676 (16.7%)
   Sandstorms: 6652 (16.6%)
   Windy: 6624 (16.6%)
   Sunny: 6504 (16.3%)

🔹 Road_traffic_density:
   Low: 13699 (34.3%)
   Jam: 12610 (31.5%)
   Medium: 9755 (24.4%)
   High: 3933 (9.8%)

🔹 Age_Category:
   Senior: 14187 (35.5%)
   Giovane: 13869 (34.7%)
   Adulto: 11941 (29.9%)

🔹 Delivery_Status:
   Ritardo: 30125 (75.3%)
   Puntuale: 9872 (24.7%)

======================================================================
🔗 COSTRUZIONE STRUTTURA DAG
======================================================================

📐 Struttura del modello:
--------------------------------------------------

                    ┌─────────────────────┐
                    │ Weather_conditions  │
                    └─────────┬───────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               │               │
    ┌─────────────────────┐   │               │
    │Road_traffic_density │   │               │
    └─────────┬───────────┘   │               │
              │               │               │
              │               ▼               │
              │    ┌─────────────────────┐    │
              └───►│  Delivery_Status    │◄───┘
                   └─────────────────────┘
                             ▲
                             │
                   ┌─────────────────────┐
                   │    Age_Category     │
                   └─────────────────────┘
    
🔗 Archi definiti:
   Weather_conditions → Road_traffic_density
   Weather_conditions → Delivery_Status
   Road_traffic_density → Delivery_Status
   Age_Category → Delivery_Status

======================================================================
🎓 TASK 3: APPRENDIMENTO PARAMETRI (MLE)
======================================================================

⏳ Training in corso con MaximumLikelihoodEstimator...
✅ Training completato!

----------------------------------------------------------------------
📊 CONDITIONAL PROBABILITY TABLES (CPT)
----------------------------------------------------------------------

============================================================
🚗 CPT: Road_traffic_density | Weather_conditions
============================================================
(Mostra come il meteo influenza la densità del traffico)

Traffico        | Cloudy       | Fog          | Sandstorms   | Stormy       | Sunny        | Windy        | 
----------------------------------------------------------------------------------------------------------
High            |        9.8% |       10.1% |        9.3% |        9.7% |       10.1% |       10.0% | 
Jam             |       31.2% |       31.9% |       32.0% |       30.7% |       31.6% |       31.8% | 
Low             |       34.6% |       33.8% |       34.6% |       35.2% |       33.8% |       33.4% | 
Medium          |       24.4% |       24.2% |       24.0% |       24.4% |       24.5% |       24.9% | 

💡 Interpretazione:
   - La tabella mostra P(Traffico | Meteo)
   - Ogni colonna somma a 100%

============================================================
📦 CPT: Delivery_Status | Weather, Traffic, Age
============================================================
(Mostra come i fattori influenzano il ritardo)

📋 Tabella completa (formato pgmpy):
------------------------------------------------------------
+---------------------------+-----+------------------------------+
| Age_Category              | ... | Age_Category(Senior)         |
+---------------------------+-----+------------------------------+
| Road_traffic_density      | ... | Road_traffic_density(Medium) |
+---------------------------+-----+------------------------------+
| Weather_conditions        | ... | Weather_conditions(Windy)    |
+---------------------------+-----+------------------------------+
| Delivery_Status(Puntuale) | ... | 0.059625212947189095         |
+---------------------------+-----+------------------------------+
| Delivery_Status(Ritardo)  | ... | 0.9403747870528109           |
+---------------------------+-----+------------------------------+

📊 Casi rappresentativi (probabilità di RITARDO):
---------------------------------------------------------------------------

Meteo        | Traffico | Età        | P(Ritardo)  
-------------------------------------------------------
Cloudy       | High     | Adulto     |       94.4%
Cloudy       | High     | Giovane    |       95.3%
Cloudy       | Jam      | Adulto     |       94.9%
Cloudy       | Jam      | Giovane    |       94.8%
Fog          | High     | Adulto     |       93.8%
Fog          | High     | Giovane    |       96.0%

----------------------------------------------------------------------
✔️  VALIDAZIONE MODELLO
----------------------------------------------------------------------
✅ Il modello è VALIDO!
   - Tutte le CPT sono correttamente definite
   - Le probabilità sommano a 1 per ogni configurazione
   - Il DAG è aciclico

======================================================================
🔮 TASK 4: MOTORE DI INFERENZA
======================================================================

⚙️  Inizializzazione Variable Elimination...
✅ Motore di inferenza pronto!

======================================================================
🎬 ESECUZIONE SCENARI DI INFERENZA
======================================================================

📋 Stati disponibili nel dataset:
   • Weather: ['Fog', 'Stormy', 'Sunny', 'Windy', 'Sandstorms', 'Cloudy']
   • Traffic: ['Low', 'Jam', 'Medium', 'High']
   • Age: ['Giovane', 'Adulto', 'Senior']

──────────────────────────────────────────────────────────────────────
🔍 SCENARIO A: Analisi Rischio - PREDIZIONE (Caso Estremo)
──────────────────────────────────────────────────────────────────────
📝 Domanda: Dato che c'è TEMPESTA, l'autista è GIOVANE e c'è INGORGO,
           qual è la probabilità di Ritardo?

📋 Evidenze fornite:
   • Weather_conditions = 'Stormy'
   • Age_Category = 'Giovane'
   • Road_traffic_density = 'Jam'

🎯 Query: P(Delivery_Status | evidenze)

📊 RISULTATI:
----------------------------------------
   Puntuale       :  17.30% |█████░░░░░░░░░░░░░░░░░░░░░░░░░| 
   Ritardo        :  82.70% |████████████████████████░░░░░░| ◄── PIÙ PROBABILE

💡 Interpretazione Scenario A:
   🔴 ALTO RISCHIO! Con 82.7% di probabilità di ritardo,
   questa combinazione è sfavorevole per la puntualità.

──────────────────────────────────────────────────────────────────────
🔍 SCENARIO B: Analisi Rischio - SITUAZIONE IDEALE
──────────────────────────────────────────────────────────────────────
📝 Domanda: Dato che c'è SOLE, l'autista è SENIOR e il traffico è BASSO,
           qual è la probabilità di Ritardo?

📋 Evidenze fornite:
   • Weather_conditions = 'Sunny'
   • Age_Category = 'Senior'
   • Road_traffic_density = 'Low'

🎯 Query: P(Delivery_Status | evidenze)

📊 RISULTATI:
----------------------------------------
   Puntuale       :  47.05% |██████████████░░░░░░░░░░░░░░░░| 
   Ritardo        :  52.95% |███████████████░░░░░░░░░░░░░░░| ◄── PIÙ PROBABILE

💡 Interpretazione Scenario B:
   🟡 Puntualità stimata: 47.1%

📈 CONFRONTO Scenario A vs B:
   Rischio Ritardo: 82.7% (pessimo) vs 52.9% (ottimo)
   Differenza: 29.7 punti percentuali!

──────────────────────────────────────────────────────────────────────
🔍 SCENARIO C: DIAGNOSI - Ragionamento Inverso (Sherlock Holmes)
──────────────────────────────────────────────────────────────────────
📝 Domanda: Il pacco è arrivato in RITARDO e l'autista era ESPERTO (Adulto).
           Qual era la probabile densità del traffico?

📋 Evidenze fornite:
   • Delivery_Status = 'Ritardo'
   • Age_Category = 'Adulto'

🎯 Query: P(Road_traffic_density | evidenze)

📊 RISULTATI:
----------------------------------------
   High           :  10.75% |███░░░░░░░░░░░░░░░░░░░░░░░░░░░| 
   Jam            :  35.87% |██████████░░░░░░░░░░░░░░░░░░░░| ◄── PIÙ PROBABILE
   Low            :  27.11% |████████░░░░░░░░░░░░░░░░░░░░░░| 
   Medium         :  26.28% |███████░░░░░░░░░░░░░░░░░░░░░░░| 

💡 Interpretazione Scenario C (Ragionamento Diagnostico):
   🔍 Traffico più probabile dato il ritardo: Jam
      con probabilità 35.9%
   📊 Probabilità traffico intenso (Jam + High): 46.6%

======================================================================
📊 ANALISI AGGIUNTIVE
=================================================================å=====

🌤️  Effetto del METEO sul rischio di ritardo:
--------------------------------------------------

Meteo           | P(Ritardo)   | P(Puntuale)  | Rischio
------------------------------------------------------------
☁️ Cloudy       |       80.9% |       19.1% | 🔴 ALTO
🌫️ Fog          |       79.4% |       20.6% | 🔴 ALTO
🏜️ Sandstorms   |       77.4% |       22.6% | 🔴 ALTO
⛈️ Stormy       |       77.3% |       22.7% | 🔴 ALTO
☀️ Sunny        |       59.0% |       41.0% | 🔴 ALTO
💨 Windy        |       77.5% |     å  22.5% | 🔴 ALTO


👤 Effetto dell'ESPERIENZA dell'autista:
--------------------------------------------------

Categoria    | P(Ritardo)   | P(Puntuale)  | Affidabilità
-----------------------------------------------------------------
👨 Adulto     |       75.2% |       24.8% | ⭐ BASSA
🧑 Giovane    |       62.8% |       37.2% | ⭐ BASSA
👴 Senior     |       87.7% |       12.3% | ⭐ BASSA


🔮 DIAGNOSI: Se c'è ritardo, qual era probabilmente il meteo?
--------------------------------------------------

Meteo           | P(Meteo | Ritardo)
----------------------------------------
☁️ Cloudy       |   17.9% |████
🌫️ Fog          |   17.9% |████
🏜️ Sandstorms   |   17.1% |████
⛈️ Stormy       |   17.3% |████
☀️ Sunny        |   12.7% |███
💨 Windy        |   17.0% |████

======================================================================
📋 RIEPILOGO ESECUZIONE
======================================================================

    ✅ Task 3 Completato:
       • Modello addestrato con Maximum Likelihood Estimation
       • CPT generate per tutti i nodi
       • Modello validato con successo
       • Dataset utilizzato: 39997 record
         - Puntuali: 9872 (24.7%)
         - Ritardi: 30125 (75.3%)

    ✅ Task 4 Completato:
       • Motore di inferenza Variable Elimination configurato
       • Scenario A (Predizione Pessimistica): Analizzato
       • Scenario B (Predizione Ottimistica): Analizzato  
       • Scenario C (Diagnosi Inversa): Analizzato

    🎯 Insight Principali:
       • La rete bayesiana permette ragionamento probabilistico bidirezionale
       • Predizione: dalle cause (meteo, età) agli effetti (ritardo)
       • Diagnosi: dagli effetti (ritardo) alle probabili cause
```

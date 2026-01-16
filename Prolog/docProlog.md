# Documentazione Modulo Sistema Esperto (Prolog)

## SEZIONE 1: Sommario
Il modulo in esame affronta la problematica del supporto decisionale automatizzato nel contesto della logistica di distribuzione. Nello specifico, si implementa un Sistema Esperto basato su regole logiche per la gestione delle criticità nelle consegne, integrando paradigmi di programmazione imperativa (Python) e logica (Prolog).

L'**input** del sistema è costituito da un dataset strutturato (`bayesian_training_data.csv`) che racchiude osservazioni storiche sulle consegne dell'ultimo miglio. Le variabili considerate includono le condizioni meteorologiche (*Weather_conditions*), la densità del traffico (*Road_traffic_density*), la categoria di età del conducente (*Age_Category*) e lo stato corrente della consegna (*Delivery_Status*).

L'**output** atteso è la generazione automatica di una Knowledge Base (KB) in formato Prolog (`sistema_esperto.pl`). Questo artefatto contiene sia i "fatti", derivati direttamente dalla trasposizione delle osservazioni empiriche del dataset, sia un corpus di "regole" di business codificate logicamente.

L'**obiettivo** del sistema è formalizzare la logica di dominio per permettere deduzioni automatiche su azioni correttive (quali l'annullamento dell'ordine per sicurezza o il supporto proattivo all'autista) interrogando la base di conoscenza in modo dichiarativo, separando così la logica di controllo dai dati.

## SEZIONE 2: Strumenti utilizzati
Per lo sviluppo del generatore della Knowledge Base e la definizione del sistema esperto sono state impiegate le seguenti tecnologie:

*   **Pandas**: Libreria fondamentale per la manipolazione dati, utilizzata qui per l'ingestione del file CSV, la gestione dei dati mancanti e l'iterazione sulle istanze per la creazione dinamica dei fatti Prolog.
*   **OS (Python Standard Library)**: Utilizzata per garantire la portabilità del codice attraverso la gestione agnostica dei percorsi dei file system e per le operazioni di scrittura del file di output.
*   **Sintassi Prolog (Standard ISO)**: Il codice Python genera stringhe formattate secondo la sintassi standard Prolog (comprendente atomi, predicati e clausole di Horn), rendendo il risultato compatibile con interpreti come SWI-Prolog o ambienti web come SWISH.

## SEZIONE 3: Decisioni di Progetto
Il design del sistema segue un approccio ibrido, delegando a Python il compito di **ETL (Extract, Transform, Load)** e a Prolog quello di **motore inferenziale**.

Per quanto riguarda il **trattamento dei dati**, viene implementata una specifica pipeline di normalizzazione. I valori categorici grezzi estratti dal dataset (spesso contenenti spazi o caratteri maiuscoli) vengono trasformati in "atomi" Prolog validi mediante conversione in minuscolo (*lowercase*) e sostituzione degli spazi con underscore (es. "High Jam" $\to$ `high_jam`). Viene inoltre gestita la robustezza del dato: eventuali valori nulli (*NaN*) vengono mappati sul letterale `unknown` per evitare errori di sintassi nella KB.

La **scelta algoritmica** ricade su un **Sistema Basato su Regole (Rule-Based System)** deterministico. A differenza di approcci probabilistici o di machine learning puro, questo modello garantisce che a specifiche precondizioni corrisponda sempre un'azione univoca e spiegabile, requisito critico per le policy aziendali di sicurezza.

La **modellazione del problema** si basa sul predicato n-ario `consegna(ID, Meteo, Traffico, EtaAutista, Status)`, che reifica ogni riga del dataset in un fatto logico. Le regole decisionali sono definite tramite il predicato `azione(ID, Azione)`, strutturato gerarchicamente con l'uso del *cut* (`!`) per implementare priorità:

1.  **Sicurezza**: Priorità massima. Se il meteo è avverso (*stormy*, *sandstorms*) e c'è ritardo, l'azione è `annulla_e_riprogramma`.
    ```prolog
    azione(ID, annulla_e_riprogramma) :-
        consegna(ID, Meteo, _, _, ritardo),
        (Meteo = stormy ; Meteo = sandstorms),
        !.
    ```
2.  **Supporto**: Se il traffico è critico e l'autista è giovane/inesperto, l'azione è `contatta_autista`.
    ```prolog
    azione(ID, contatta_autista) :-
        consegna(ID, _, Traffico, giovane, _),
        (Traffico = jam ; Traffico = high),
        !.
    ```
3.  **Performance**: Se il meteo è favorevole (*sunny*) ma c'è ritardo, scatta la `segnalazione_performance`.
    ```prolog
    azione(ID, segnalazione_performance) :-
        consegna(ID, sunny, _, _, ritardo),
        !.
    ```
4.  **Default**: In assenza di condizioni critiche, l'azione è `procedere`.
    ```prolog
    azione(ID, procedere) :-
        consegna(ID, _, _, _, _),
        \+ azione_speciale(ID).
    ```


## SEZIONE 4: Valutazione
La valutazione del modulo consiste nella verifica della coerenza logica della Knowledge Base generata e nella capacità del sistema di classificare correttamente le situazioni operative.

Dall'analisi dell'esecuzione, il sistema processa con successo le prime 20 istanze del dataset (parametro configurabile tramite `df.head(20)`), traducendole in altrettanti fatti Prolog. Il corpus di regole implementato copre il 100% dei casi possibili grazie alla clausola di default ("closed-world assumption").

Il modulo non produce metriche quantitative di errore (come accuratezza o F1-score) in quanto opera in un dominio logico deduttivo e non induttivo. Tuttavia, l'efficacia del sistema è dimostrata dalla generazione di query di utilità pre-assemblate (es. `consegne_da_annullare/1`), che permettono agli operatori di filtrare istantaneamente sottoinsiemi critici di ordini. Le istruzioni generate per l'ambiente SWISH confermano che il codice prodotto è sintatticamente corretto e pronto per l'interrogazione in un motore Prolog standard.

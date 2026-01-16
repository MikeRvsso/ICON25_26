# Report Tecnico: Modulo di Ricerca (Routing)

## 1. Sommario

Il modulo implementa un sistema di pianificazione del percorso (Routing) modellato come un **Problema del Commesso Viaggiatore (TSP)**. L'obiettivo pratico è determinare l'ordine ottimale di visita per un veicolo di consegna, partendo da un deposito, visitando tutti i punti assegnati una sola volta e facendo ritorno alla base.

**Input**: L'input è costituito dal dataset `amazon_delivery_optimized.csv`, da cui vengono estratti gli ordini specifici per il **Furgone 0** (39 pacchi nello stato 'Loaded').

**Output**: L'output atteso è duplice:
- Un file CSV (`route_van_0.csv`) contenente la sequenza ordinata delle consegne.
- Una mappa interattiva (`delivery_route_map.html`) per la visualizzazione geografica del tragitto.

**Obiettivo**: L'obiettivo dell'algoritmo è minimizzare la distanza totale percorsa, riducendo così i costi operativi e i tempi di consegna, sebbene l'approccio scelto privilegi la velocità di calcolo rispetto all'ottimalità globale assoluta.

## 2. Strumenti utilizzati

Il codice fa uso delle seguenti librerie Python principali:

- **Pandas**: Utilizzata per il caricamento, il filtraggio dei dati (selezione del Van 0) e l'esportazione del percorso finale in formato CSV.
- **Numpy**: Impiegata per operazioni numeriche efficienti, in particolare per calcolare il centroide delle coordinate (media di latitudine/longitudine) per definire la posizione del deposito.
- **Math**: Fornisce le funzioni trigonometriche (`sin`, `cos`, `atan2`, `radians`) necessarie per l'implementazione della formula dell'Haversine.
- **Folium**: Usata per la generazione della mappa interattiva HTML, permettendo la visualizzazione dei marker e del tracciato del percorso su mappa reale.
- **Dataclasses**: Utilizzata per definire la struttura dati `DeliveryNode` in modo conciso e leggibile.

## 3. Decisioni di Progetto

Il progetto adotta un approccio basato sulla ricerca locale informata per risolvere il problema di ottimizzazione.

**Trattamento dei Dati**: 
I dati vengono caricati dal output del modulo CSP precedente. Viene effettuata una fase di preprocessing in cui si filtrano solo i pacchi assegnati al furgone target. Il **Deposito** non è un punto statico nel dataset, ma viene calcolato dinamicamente come baricentro (media delle coordinate) di tutti i punti di consegna, simulando un punto di partenza centrale ottimale per il cluster di consegne.

**Algoritmo Scelto**: 
È stato implementato l'algoritmo **Greedy Best-First Search (GBFS)**. La scelta è ricaduta su un approccio *greedy* (avido) per la sua efficienza computazionale rispetto a soluzioni esatte (come Branch & Bound) su istanze di medie dimensioni. Il codice esplicitamente nota che questo approccio garantisce una soluzione rapida ma non necessariamente l'ottimo globale.

**Modellazione del Problema**: 
Il dominio è modellato come un grafo in cui i nodi rappresentano i punti di consegna (`DeliveryNode`) e gli archi rappresentano il cammino diretto tra loro. Il grafo è trattato come completamente connesso (si può andare da qualsiasi punto a qualsiasi altro).

**Parametri e Euristiche**: 
La funzione euristica $h(n)$ utilizzata è la **Distanza di Haversine** (distanza in linea d'aria su superficie sferica). Ad ogni passo, l'algoritmo seleziona il nodo *non visitato* che minimizza questa distanza rispetto alla posizione corrente, senza considerare il costo del cammino futuro (differenza chiave rispetto ad A*).

## 4. Valutazione

Dall'esecuzione del codice sul dataset di test (Furgone 0 con 39 pacchi), emergono i seguenti risultati:

**Metriche di Performance**: 
L'algoritmo ha calcolato un percorso completo che copre una distanza totale di **1584.98 km**.

**Analisi del Percorso**: 
Il processo di ottimizzazione ha richiesto **40 passi** (39 consegne + ritorno al deposito). I log di esecuzione evidenziano il comportamento tipico degli algoritmi greedy: riesce spesso a trovare nodi molto vicini (passi con 0.00 km o poche centinaia di metri), ma occasionalmente è costretto a "salti" lunghi (es. Passo 34: 733.92 km, Passo 28: 324.22 km). Questo accade perché la strategia avida può condurre a minimi locali, lasciando punti isolati da visitare necessariamente alla fine del percorso.

**Output Generati**: 
Il sistema ha prodotto con successo:
- `delivery_route_map.html`: Visualizza il percorso con una *PolyLine* blu e marker numerati.
- `route_van_0.csv`: Contiene il piano di viaggio per l'uso logistico.

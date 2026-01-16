# Documentazione Modulo Supervised Learning

## SEZIONE 1: Sommario

Il modulo di Machine Learning implementato affronta un problema di **Regressione**, con l'obiettivo di predire in modo accurato il tempo di consegna stimato (`Delivery_Time`) per gli ordini Amazon. L'input del sistema è costituito dal dataset pre-elaborato (`amazon_delivery_final.csv`), che contiene vettori di caratteristiche relativi a ogni singolo ordine, incluse variabili ambientali (meteo, traffico) e logistiche (tipo di veicolo, distanza, densità di agenti). L'output atteso è una variabile continua rappresentante il tempo in minuti necessario per il completamento della consegna. L'obiettivo primario dell'architettura è la minimizzazione dell'errore quadratico medio (MSE) e la massimizzazione del coefficiente di determinazione ($R^2$), al fine di fornire stime temporali affidabili per l'ottimizzazione della catena logistica successiva.

## SEZIONE 2: Strumenti utilizzati

La realizzazione del modulo si avvale dello stack scientifico Python standard:
*   **Pandas**: Utilizzato per il caricamento, la pulizia e la manipolazione strutturata dei dati tabulari.
*   **NumPy**: Supporta le operazioni algebriche e statistiche sui vettori numerici.
*   **Scikit-learn**: Costituisce il nucleo algoritmico, fornendo le implementazioni per `LinearRegression`, `DecisionTreeRegressor` e `RandomForestRegressor`, oltre alle utility per il partizionamento dei dati (`train_test_split`) e la validazione incrociata (`cross_val_score`).
*   **XGBoost**: Libreria ottimizzata utilizzata per implementare e testare algoritmi avanzati di Gradient Boosting.
*   **Joblib**: Utilizzata per la serializzazione (persistenza) e il caricamento dei modelli addestrati.

## SEZIONE 3: Decisioni di Progetto

### Trattamento dei dati
Il trattamento dei dati inizia con una fase di pulizia preliminare in cui viene rimossa la colonna identificativa `Order_ID`, priva di valore predittivo, e si separano le feature (matrice $X$) dalla variabile target (vettore $y$). Per garantire una valutazione imparziale, il dataset viene suddiviso staticamente in un Training Set (80%) e un Test Set (20%), mantenendo un `random_state` fisso per la riproducibilità degli esperimenti. Nel caso specifico dei modelli sensibili alla scala come la Regressione Lineare, è stata applicata una standardizzazione delle feature tramite `StandardScaler`, mentre per gli algoritmi basati su alberi si è proceduto direttamente sui dati grezzi, sfruttando la loro invarianza di scala.

### Selezione dell'Algoritmo
La selezione dell'algoritmo di predizione è stata guidata da un approccio comparativo rigoroso:
1.  **Baseline**: Inizialmente è stata definita una baseline utilizzando una *Regressione Lineare*, i cui risultati hanno evidenziato la natura non lineare delle relazioni tra le variabili (come l'interazione complessa tra traffico e meteo).
2.  **Overfitting con Alberi Singoli**: Successivamente, l'impiego di un *Decision Tree* singolo senza vincoli di profondità (`max_depth=None`) ha dimostrato una forte tendenza all'overfitting, caratterizzata da un'alta varianza e scarsa capacità di generalizzazione su nuovi dati.
3.  **Random Forest**: La decisione progettuale definitiva è ricaduta sul *Random Forest Regressor*, configurato con 100 stimatori (`n_estimators=100`). La scelta è motivata dalla capacità di questo algoritmo di ridurre la varianza attraverso la tecnica del *Bagging* (Bootstrap Aggregating), mediando le predizioni di molteplici alberi decorrelati.

Per validare la robustezza del modello e scongiurare bias di campionamento, è stata implementata una **K-Fold Cross Validation** con $K=5$, che ha confermato la stabilità delle performance attraverso diverse partizioni del training set. Sebbene sia stato testato anche l'algoritmo **XGBoost** (Gradient Boosting), che ha offerto un leggero incremento prestazionale lavorando sulla riduzione del *bias*, si è preferito mantenere il Random Forest per il prototipo finale in virtù del miglior bilanciamento tra accuratezza, interpretabilità e facilità di implementazione.

## SEZIONE 4: Valutazione

La valutazione delle performance è stata condotta utilizzando metriche standard per problemi di regressione: Mean Squared Error (MSE), Root Mean Squared Error (RMSE) e Coefficiente di Determinazione ($R^2$).

L'analisi comparativa ha prodotto i seguenti risultati quantitativi:

*   **Regressione Lineare (Baseline)**: Il modello ha ottenuto un $R^2$ di circa **0.61**, dimostrando l'insufficienza di un approccio lineare per catturare circa il 40% della variabilità dei dati.
*   **Decision Tree**: L'esperimento ha mostrato un $R^2$ prossimo a 1.0 sul training set ma un crollo significativo delle prestazioni sul test set (intorno a 0.50), confermando un grave overfitting.
*   **Random Forest (Modello Scelto)**: Il modello ha raggiunto un $R^2$ di **0.73** sul Test Set. La validazione incrociata ha evidenziato una deviazione standard contenuta ($< 0.05$), indicando un'ottima stabilità e assenza di overfitting significativo (la differenza tra Score nel CV e nel Test Set è minima).
*   **XGBoost**: Ha registrato le performance migliori in assoluto con un $R^2$ di **0.757** e un RMSE di **0.49**, confermando che il boosting riesce a catturare pattern marginalmente più complessi rispetto al bagging.

Al termine del processo, il modello finale è stato serializzato nel file `delivery_model.pkl` e le predizioni sull'intero dataset sono state esportate in `amazon_delivery_with_predictions.csv` per le fasi successive del progetto.

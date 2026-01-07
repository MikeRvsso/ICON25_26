# 🚚 Vehicle Routing & Bin Packing - Report

**Data esecuzione:** 06/01/2026 23:14:05

**Progetto:** Amazon Delivery AI - Ottimizzazione Flotta

---

## Output Completo

```

🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀

   AMAZON DELIVERY - VEHICLE ROUTING OPTIMIZATION
   Ricerca Operativa: Bin Packing & Clustering

🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
============================================================
CARICAMENTO DATI
============================================================
✓ File caricato: ../Supervised_Learning/amazon_delivery_with_predictions.csv
✓ Numero totale consegne: 39997
✓ Colonne disponibili: ['Order_ID', 'Agent_Age', 'Agent_Rating', 'Store_Latitude', 'Store_Longitude', 'Drop_Latitude', 'Drop_Longitude', 'Delivery_Time', 'Weather_Cloudy', 'Weather_Fog', 'Weather_Sandstorms', 'Weather_Stormy', 'Weather_Sunny', 'Weather_Windy', 'Traffic_High', 'Traffic_Jam', 'Traffic_Low', 'Traffic_Medium', 'Vehicle_motorcycle', 'Vehicle_scooter', 'Vehicle_van', 'Area_Metropolitian', 'Area_Other', 'Area_Semi-Urban', 'Area_Urban', 'Category_Apparel', 'Category_Books', 'Category_Clothing', 'Category_Cosmetics', 'Category_Electronics', 'Category_Grocery', 'Category_Home', 'Category_Jewelry', 'Category_Kitchen', 'Category_Outdoors', 'Category_Pet Supplies', 'Category_Shoes', 'Category_Skincare', 'Category_Snacks', 'Category_Sports', 'Category_Toys', 'Predicted_Time']
✓ Range Predicted_Time: [-2.191, 2.700]

============================================================
STEP 1: DE-STANDARDIZZAZIONE DEI TEMPI
============================================================

📊 Statistiche z-score originali:
   • Minimo (z_min): -2.1915
   • Massimo (z_max): 2.7003
   • Media: 0.0023
   • Deviazione Std: 0.9123

⏱️  Mapping completato:
   • z-score -2.19 → 10 minuti
   • z-score 2.70 → 120 minuti

📈 Statistiche Time_Minutes:
   • Minimo: 10 minuti
   • Massimo: 120 minuti
   • Media: 59.3 minuti
   • Mediana: 58.0 minuti

============================================================
STEP 2: CLUSTERING GEOGRAFICO (K-MEANS)
============================================================

🌍 Coordinate geografiche:
   • Latitudine: [9.9671, 31.0541]
   • Longitudine: [72.7787, 88.5635]

🚚 Clustering completato con 5 zone:
--------------------------------------------------
   Furgone 0:
      • Pacchi assegnati: 3624
      • Centro zona: (23.5889, 85.4241)
   Furgone 1:
      • Pacchi assegnati: 14125
      • Centro zona: (20.6475, 73.8870)
   Furgone 2:
      • Pacchi assegnati: 12631
      • Centro zona: (12.2669, 77.8578)
   Furgone 3:
      • Pacchi assegnati: 6006
      • Centro zona: (27.3660, 76.8248)
   Furgone 4:
      • Pacchi assegnati: 3611
      • Centro zona: (17.1955, 77.7478)

📊 Qualità clustering:
   • Inerzia (somma distanze²): 158204.21

============================================================
STEP 3: BIN PACKING OPTIMIZATION (GREEDY)
============================================================

⚙️  Vincolo: Capacità furgone = 480 minuti (8 ore)
📋 Strategia: Greedy - Priorità ai pacchi più veloci

------------------------------------------------------------

🚚 FURGONE 0:
   📦 Pacchi zona: 3624
   ✅ Caricati: 39
   ❌ Esclusi: 3585
   ⏱️  Tempo totale: 478/480 minuti
   📊 Utilizzo turno: 99.6%

🚚 FURGONE 1:
   📦 Pacchi zona: 14125
   ✅ Caricati: 44
   ❌ Esclusi: 14081
   ⏱️  Tempo totale: 478/480 minuti
   📊 Utilizzo turno: 99.6%

🚚 FURGONE 2:
   📦 Pacchi zona: 12631
   ✅ Caricati: 44
   ❌ Esclusi: 12587
   ⏱️  Tempo totale: 479/480 minuti
   📊 Utilizzo turno: 99.8%

🚚 FURGONE 3:
   📦 Pacchi zona: 6006
   ✅ Caricati: 41
   ❌ Esclusi: 5965
   ⏱️  Tempo totale: 472/480 minuti
   📊 Utilizzo turno: 98.3%

🚚 FURGONE 4:
   📦 Pacchi zona: 3611
   ✅ Caricati: 40
   ❌ Esclusi: 3571
   ⏱️  Tempo totale: 480/480 minuti
   📊 Utilizzo turno: 100.0%

============================================================
REPORT FINALE OTTIMIZZAZIONE FLOTTA
============================================================

📊 STATISTICHE GLOBALI:
   • Pacchi totali nel dataset: 39997
   • Pacchi caricati (Loaded): 208 (0.5%)
   • Pacchi esclusi (Skipped): 39789 (99.5%)

📋 RIEPILOGO PER FURGONE:
----------------------------------------------------------------------
Furgone    Caricati     Tempo (min)     Utilizzo %   Efficienza  
----------------------------------------------------------------------
Van 0      39           478             99.6         🟢 Ottimo    
Van 1      44           478             99.6         🟢 Ottimo    
Van 2      44           479             99.8         🟢 Ottimo    
Van 3      41           472             98.3         🟢 Ottimo    
Van 4      40           480             100.0        🟢 Ottimo    
----------------------------------------------------------------------

🚛 EFFICIENZA FLOTTA:
   • Capacità totale flotta: 2400 minuti (40 ore)
   • Tempo totale utilizzato: 2387 minuti (39.8 ore)
   • Utilizzo medio flotta: 99.5%

💡 RACCOMANDAZIONI:
   ⚠️  39789 pacchi richiedono un turno aggiuntivo o furgoni extra
   ✅ Flotta ottimizzata al massimo della capacità

💾 Salvataggio risultati...
✅ File salvato: amazon_delivery_optimized.csv

📄 Preview colonne aggiunte:
       Predicted_Time  Time_Minutes  Van_ID   Status
1854        -2.071123            13       0  Skipped
18936       -2.079787            13       0  Skipped
25882       -2.047441            13       0  Skipped
26717       -2.068427            13       0  Skipped
27066       -2.036659            13       0  Skipped
31884       -2.052447            13       0  Skipped
32323       -2.055142            13       0  Skipped
2092        -2.014710            14       0  Skipped
5519        -2.004120            14       0  Skipped
7940        -1.998152            14       0  Skipped

============================================================
✅ OTTIMIZZAZIONE COMPLETATA CON SUCCESSO!
============================================================


```

---

## Parametri Configurazione

| Parametro | Valore |
|-----------|--------|
| Numero Furgoni | 5 |
| Capacità per Furgone | 480 minuti (8 ore) |
| Tempo Min Consegna | 10 minuti |
| Tempo Max Consegna | 120 minuti |

---

## Metodologia

### Step 1: De-Standardizzazione
Mapping lineare dei z-score → minuti reali [10, 120]

### Step 2: Clustering Geografico
K-Means con k=5 per divisione territoriale

### Step 3: Bin Packing Greedy
Ottimizzazione carico con priorità ai pacchi più veloci

---

*Report generato automaticamente dal sistema di ottimizzazione flotta*

% KNOWLEDGE BASE AZIENDALE - POLICY LOGISTICHE MUMBAI

% --- FATTI (Estratti dal Dataset) ---
agente(agente_1, 4.7, 'Urban').
agente(agente_2, 4.8, 'Metropolitian').
agente(agente_3, 4.8, 'Urban').
agente(agente_4, 4.9, 'Metropolitian').
agente(agente_5, 4.6, 'Urban').

ordine(hroe078436861, 'Cloudy', 'Medium', 'Pet Supplies').
ordine(cjhk414294530, 'Sandstorms', 'Jam', 'Snacks').
ordine(qkux956576156, 'Stormy', 'Medium', 'Grocery').
ordine(jqlw124491584, 'Sandstorms', 'Low', 'Cosmetics').
ordine(xqmf197034060, 'Windy', 'Medium', 'Electronics').

% --- FATTI AUSILIARI (Definizione Dominio Critico) ---
meteo_critico('Stormy').
meteo_critico('Fog').
meteo_critico('Sandstorms').

traffico_critico('Jam').
traffico_critico('High').

% --- REGOLE DI BUSINESS (Logica Deduttiva) ---

% Regola 1: Bonus Merito
% Un agente ottiene il bonus se ha un rating >= 4.7 e opera nell'area Metropolitian.
assegna_bonus(A) :-
    agente(A, R, 'Metropolitian'),
    R >= 4.7.

% Regola 2: Alert Logistico
% Segnala un ordine se si trova in condizioni di doppio rischio (meteo e traffico critici).
notifica_ritardo(O) :-
    ordine(O, W, T, _),
    meteo_critico(W),
    traffico_critico(T).

% Regola 3: Gestione Priorità
% Un ordine ha priorità alta se contiene elettronica.
priorita_alta(O) :-
    ordine(O, _, _, 'Electronics').

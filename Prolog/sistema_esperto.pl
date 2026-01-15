% ============================================
% SISTEMA ESPERTO - Logistica Amazon
% Knowledge Base generata automaticamente da Python
% ============================================
%
% Struttura: consegna(ID, Meteo, Traffico, EtaAutista, Status)
%
% Regole di Business:
%   1. Sicurezza: annulla con maltempo + ritardo
%   2. Supporto: contatta autista giovane in traffico critico
%   3. Performance: segnala ritardi ingiustificati
%   4. Default: procedere normalmente
%
% ============================================

% ============================================
% FATTI - Dati delle consegne
% consegna(ID, Meteo, Traffico, EtaAutista, Status)
% ============================================

consegna(ord_0, windy, medium, adulto, puntuale).
consegna(ord_1, sunny, low, senior, ritardo).
consegna(ord_2, sunny, medium, adulto, puntuale).
consegna(ord_3, windy, jam, giovane, puntuale).
consegna(ord_4, fog, medium, senior, puntuale).
consegna(ord_5, cloudy, jam, adulto, ritardo).
consegna(ord_6, cloudy, high, senior, ritardo).
consegna(ord_7, cloudy, low, giovane, ritardo).
consegna(ord_8, windy, medium, adulto, ritardo).
consegna(ord_9, sunny, jam, giovane, puntuale).
consegna(ord_10, windy, high, senior, ritardo).
consegna(ord_11, windy, high, adulto, ritardo).
consegna(ord_12, sandstorms, medium, senior, puntuale).
consegna(ord_13, sunny, medium, senior, ritardo).
consegna(ord_14, sandstorms, high, adulto, puntuale).
consegna(ord_15, stormy, low, senior, puntuale).
consegna(ord_16, sunny, low, giovane, puntuale).
consegna(ord_17, sunny, jam, senior, puntuale).
consegna(ord_18, sunny, low, giovane, ritardo).
consegna(ord_19, cloudy, high, giovane, ritardo).

% ============================================
% REGOLE DI BUSINESS - Sistema Esperto Logistica
% ============================================

% ------------------------------------------
% REGOLA 1: SICUREZZA
% Condizione: meteo estremo (stormy/sandstorms) E consegna in ritardo
% Azione: annullare e riprogrammare la consegna
% Motivazione: Troppo pericoloso guidare col maltempo se già in ritardo
% ------------------------------------------
azione(ID, annulla_e_riprogramma) :-
    consegna(ID, Meteo, _, _, ritardo),
    (Meteo = stormy ; Meteo = sandstorms),
    !.

% ------------------------------------------
% REGOLA 2: SUPPORTO
% Condizione: traffico critico (jam/high) E autista giovane
% Azione: contattare l'autista per fornire supporto
% Motivazione: Autista inesperto in traffico critico necessita supporto dalla centrale
% ------------------------------------------
azione(ID, contatta_autista) :-
    consegna(ID, _, Traffico, giovane, _),
    (Traffico = jam ; Traffico = high),
    !.

% ------------------------------------------
% REGOLA 3: PERFORMANCE
% Condizione: meteo buono (sunny) E consegna in ritardo
% Azione: segnalazione performance negativa
% Motivazione: Ritardo ingiustificato col bel tempo, flaggare driver
% ------------------------------------------
azione(ID, segnalazione_performance) :-
    consegna(ID, sunny, _, _, ritardo),
    !.

% ------------------------------------------
% REGOLA 4: DEFAULT
% Condizione: nessuna delle regole precedenti si applica
% Azione: procedere normalmente con la consegna
% ------------------------------------------
azione(ID, procedere) :-
    consegna(ID, _, _, _, _),
    \+ azione_speciale(ID).

% Predicato ausiliario per verificare azioni speciali
azione_speciale(ID) :-
    consegna(ID, Meteo, _, _, ritardo),
    (Meteo = stormy ; Meteo = sandstorms).
azione_speciale(ID) :-
    consegna(ID, _, Traffico, giovane, _),
    (Traffico = jam ; Traffico = high).
azione_speciale(ID) :-
    consegna(ID, sunny, _, _, ritardo).

% ============================================
% QUERY DI UTILITA'
% ============================================

% Trova tutte le consegne da annullare per sicurezza
consegne_da_annullare(Lista) :-
    findall(ID, azione(ID, annulla_e_riprogramma), Lista).

% Trova tutti gli autisti da contattare
autisti_da_contattare(Lista) :-
    findall(ID, azione(ID, contatta_autista), Lista).

% Trova tutte le segnalazioni performance
segnalazioni_performance(Lista) :-
    findall(ID, azione(ID, segnalazione_performance), Lista).

% Report completo con dettagli
report_consegna(ID, Meteo, Traffico, Eta, Status, Azione) :-
    consegna(ID, Meteo, Traffico, Eta, Status),
    azione(ID, Azione).

% Conta azioni per tipo
conta_azioni(TipoAzione, Conteggio) :-
    findall(ID, azione(ID, TipoAzione), Lista),
    length(Lista, Conteggio).

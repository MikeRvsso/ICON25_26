# main.py
import sys
# Importa i tuoi moduli (che creeremo passo passo)
# import ml_module
# import csp_module
# import search_module
# import bayes_module

def main():
    print("=== SISTEMA DI CONSEGNA INTELLIGENTE (Amazon Delivery) ===")
    
    while True:
        print("\nScegli un'operazione:")
        print("1. [ML] Addestra Modello e Predici Tempi (Supervisionato)")
        print("2. [CSP] Seleziona Pacchi per il Furgone (Vincoli)")
        print("3. [SEARCH] Calcola Percorso Ottimo (A*)")
        print("4. [BAYES] Valuta Rischio Spedizione (Probabilistico)")
        print("5. [PROLOG] Verifica Vincoli Logici")
        print("0. Esci")
        
        scelta = input("Inserisci numero: ")
        
        if scelta == '1':
            print("Avvio addestramento...")
            # ml_module.train_and_predict()
        elif scelta == '2':
            print("Selezione carico ottimale...")
            # csp_module.solve_knapsack()
        elif scelta == '3':
            print("Calcolo rotta...")
            # search_module.find_route()
        elif scelta == '0':
            print("Uscita.")
            sys.exit()
        else:
            print("Scelta non valida.")

if __name__ == "__main__":
    main()
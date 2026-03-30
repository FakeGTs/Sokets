# Client TCP multithread che invia NUM_WORKERS richieste contemporanee al server
# Ogni richiesta contiene un'operazione aritmetica da eseguire

import socket         # Per la comunicazione di rete
import json           # Per la codifica/decodifica JSON
import random         # Per generare numeri casuali
import time           # Per misurare i tempi di esecuzione
import threading      # Per gestire l'esecuzione parallela (multithreading)

# --- Configurazione ---
HOST = "127.0.0.1"           # IP del server
PORT = 65432                # Porta del server (assicurarsi che il server stia ascoltando su questa)
NUM_WORKERS = 15            # Numero di richieste (thread) da inviare in parallelo
OPERAZIONI = ["+", "-", "*", "/", "%"]  # Lista delle operazioni consentite

#1 Questa funzione genera richieste aritmetiche casuali e le invia al server, 
# poi attende la risposta e stampa il risultato insieme al tempo di esecuzione della richiesta.
def genera_richieste(address, port):
    #2 Crea un socket TCP e si connette al server specificato da address e port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_service:
        sock_service.connect((address, port))  # Connessione al server

        #3 Genera dati casuali per l'operazione da inviare al server
        primoNumero = random.randint(0, 100)
        operazione = OPERAZIONI[random.randint(0, 3)]  # Scegli operazione a caso (tra le prime 4)
        secondoNumero = random.randint(0, 100)

        #4 Crea un dizionario con i dati dell'operazione, lo converte in JSON e lo invia al server
        messaggio = {
            "primoNumero": primoNumero,
            "operazione": operazione,
            "secondoNumero": secondoNumero
        }
        messaggio = json.dumps(messaggio)

        ##5 Invia il messaggio al server utilizzando il metodo sendall() per garantire che tutto il messaggio venga inviato correttamente
        sock_service.sendall(messaggio.encode("UTF-8"))

        #6 Inizia a misurare il tempo di esecuzione della richiesta prima di attendere la risposta del server
        start_time_thread = time.time()

        #7 Attende la risposta del server e la decodifica
        data = sock_service.recv(1024)

    #8 Misura il tempo di esecuzione della richiesta dopo aver ricevuto la risposta dal server e stampa il risultato insieme al tempo impiegato
    end_time_thread = time.time()
    print("Received: ", data.decode())
    print(f"{threading.current_thread().name} exec time = ", end_time_thread - start_time_thread)

# --- Punto di ingresso del programma ---
if __name__ == "__main__":
    start_time = time.time()  # Tempo di inizio totale

    #9 Crea NUM_WORKERS thread, ognuno dei quali esegue la funzione genera_richieste per inviare richieste al server
    threads = [
        threading.Thread(target=genera_richieste, args=(HOST, PORT))
        for _ in range(NUM_WORKERS)
    ]

    #10 Avvia tutti i thread
    [thread.start() for thread in threads]

    #11 Attendi la conclusione di tutti i thread
    [thread.join() for thread in threads]

    end_time = time.time()  # Tempo di fine totale

    # Stampa il tempo complessivo impiegato per eseguire tutte le richieste
    print("Tempo totale impiegato = ", end_time - start_time)
import json
import socket

# Configurazione del server
IP = "127.0.0.1"
PORTA = 65432
DIM_BUFFER = 1024

# Creazione della socket del server con il costrutto with
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_server:
    # Binding della socket alla porta specificata
    sock_server.bind((IP, PORTA))
    # Metti la socket in ascolto per le connessioni in ingresso
    sock_server.listen()

    print(f"Server in ascolto su {IP}:{PORTA}...")

    # Loop principale del server
    while True:
        # Accetta le connessioni
        sock_service, address_client = sock_server.accept()
        print(f"Nuova connessione da {address_client}")
        
        with sock_service as sock_client:
            # Ciclo interno per gestire tutti i messaggi (i 5 inviati dal client)
            while True:
                data = sock_client.recv(DIM_BUFFER)
                # Se non ci sono più dati, il client ha chiuso la connessione
                if not data:
                    print(f"Client {address_client} disconnesso.\n")
                    break
                
                data_str = data.decode('utf-8')
                print(f"Ricevuto messaggio da {address_client}: {data_str}")

                # Deserializzazione del JSON
                dati_json = json.loads(data_str)
                primoNumero = float(dati_json["primoNumero"])
                operazione = dati_json["operazione"]
                secondoNumero = float(dati_json["secondoNumero"])

                # Calcolo
                reply = "Errore: Operazione non valida"
                if operazione == "+":
                    reply = primoNumero + secondoNumero
                elif operazione == "-":
                    reply = primoNumero - secondoNumero
                elif operazione == "*":
                    reply = primoNumero * secondoNumero
                elif operazione == "/":
                    if secondoNumero == 0:
                        reply = "Errore: Impossibile dividere per zero"
                    else:
                        reply = primoNumero / secondoNumero
                
                # Invio risposta tramite sendall (TCP) sul socket del client
                sock_client.sendall(str(reply).encode('utf-8'))
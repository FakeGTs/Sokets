import socket
import json

HOST = '127.0.0.1'  # Indirizzo del server
PORT = 65432        # Porta usata dal server
NUM_MESSAGE = 5

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_service:
    sock_service.connect((HOST, PORT))
    print("Connesso al server!\n")
    
    # Il ciclo for deve includere anche l'invio e la ricezione
    for i in range(NUM_MESSAGE):
        print(f"--- Operazione {i+1}/{NUM_MESSAGE} ---")
        primoNumero = float(input("Inserisci il primo numero: "))
        operazione = input("Inserisci l'operazione (+, -, *, /): ")
        secondoNumero = float(input("Inserisci il secondo numero: "))

        messaggio = {
                "primoNumero": primoNumero,
                "operazione": operazione,
                "secondoNumero": secondoNumero
            }
        # Serializza in JSON
        messaggio_json = json.dumps(messaggio)

        # Invio al server (TCP usa sendall, non sendto)
        sock_service.sendall(messaggio_json.encode("UTF-8"))
        print("Messaggio inviato al server, in attesa di risposta...")
            
        # Ricezione dal server (TCP usa recv, non recvfrom)
        data = sock_service.recv(1024)
        print(f"Risultato: {data.decode('utf-8')}\n")
            

print("Tutte le operazioni completate. Connessione chiusa.")
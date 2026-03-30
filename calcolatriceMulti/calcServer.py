import socket
import json
from threading import Thread

def ricevi_comandi(sock_service, addr_client):
    print(f"[+] Nuova connessione stabilita con {addr_client}")
    
    while True:
        try:
            # Uso recv() per il TCP
            data = sock_service.recv(1024)
            
            # Se data è vuoto, il client ha chiuso la connessione
            if not data:
                print(f"[-] Il client {addr_client} si è disconnesso.")
                break 
                
            messaggio = data.decode("UTF-8")
            print(f"Messaggio ricevuto dal client {addr_client}: {messaggio}")
            
            messaggio = json.loads(messaggio)
            primoNumero = messaggio["primoNumero"]
            operazione = messaggio["operazione"]
            secondoNumero = messaggio["secondoNumero"]

            if operazione == "+":
                risultato = primoNumero + secondoNumero
            elif operazione == "-":
                risultato = primoNumero - secondoNumero
            elif operazione == "*":
                risultato = primoNumero * secondoNumero
            elif operazione == "/":
                if secondoNumero != 0:
                    risultato = primoNumero / secondoNumero
                else:
                    risultato = "Errore: divisione per zero"
            else:
                risultato = "Operazione non valida"

            # Uso send() per il TCP
            sock_service.send(str(risultato).encode("UTF-8"))
            
        except json.JSONDecodeError:
            errore = "Errore: formato JSON non valido"
            sock_service.send(errore.encode("UTF-8"))
        except Exception as e:
            print(f"[!] Errore di comunicazione con {addr_client}: {e}")
            break

    # Chiudo il socket del client quando esco dal ciclo
    sock_service.close()

def avvia_server(indirizzo, porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_server:
        sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_server.bind((indirizzo, porta))
        sock_server.listen(5)
        print(f"Server in ascolto su {indirizzo}:{porta}...")
        
        while True:
            # Accetta una nuova connessione
            sock_service, addr_client = sock_server.accept()
            try:
                # Avvia un nuovo thread per gestire il client
                # daemon=True assicura che il thread si chiuda se il server principale si arresta
                Thread(target=ricevi_comandi, args=(sock_service, addr_client), daemon=True).start()
            except Exception as e:
                print(f"Errore nell'avvio del thread per {addr_client}: {e}")

# -- Main --
if __name__ == "__main__":
    IP = "127.0.0.1"
    PORTA = 65432
    DIM_BUFFER = 1024 # Definito ma non strettamente necessario a livello globale
    
    avvia_server(IP, PORTA)
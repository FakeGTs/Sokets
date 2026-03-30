import socket
import json
from threading import Thread

def ricevi_comandi(sock_service,addr_client):
    while True:
        data,addr=sock_service.recvfrom(1024)
        messaggio=data.decode("UTF-8")
        print(f"Messaggio ricevuto dal client {addr_client}: {messaggio}")
        messaggio=json.loads(messaggio)
        primoNumero=messaggio["primoNumero"]
        operazione=messaggio["operazione"]
        secondoNumero=messaggio["secondoNumero"]

        if operazione=="+":
            risultato=primoNumero+secondoNumero
        elif operazione=="-":
            risultato=primoNumero-secondoNumero
        elif operazione=="*":
            risultato=primoNumero*secondoNumero
        elif operazione=="/":
            if secondoNumero!=0:
                risultato=primoNumero/secondoNumero
            else:
                risultato="Errore: divisione per zero"
        else:
            risultato="Operazione non valida"

        sock_service.sendto(str(risultato).encode("UTF-8"),addr_client)

def ricevi_connessioni(sock_listen):
    sock_service, addr_client=sock_listen.accept()
    try:
        Thread(target=ricevi_comandi,args=(sock_service,addr_client)).start()
    except Exception as e:
        print(f"Errore nella gestione del client {addr_client}: {e}")

def avvia_server(indirizzo,porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_server:
        sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_server.bind((indirizzo,porta))
        sock_server.listen(5)
        while True:
            ricevi_comandi(sock_server)
            print(f"Server in ascolto su {indirizzo}:{porta}...")

#-- Main --

IP="127.0.0.1"
PORTA=65432
DIM_BUFFER=1024

avvia_server(IP,PORTA)
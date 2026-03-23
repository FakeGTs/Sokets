import socket
import json

SERVER_IP="127.0.0.1"
SERVER_PORT=5005
BUFFER_SIZE=1024
NUM_MESSAGE=5

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

for i in range(NUM_MESSAGE):
  primoNumero=float(input("Inserisci il primo numero: "))
  operazione=input("Inserisci l'operazione (+, -, *, /): ")
  secondoNumero=float(input("Inserisci il secondo numero: "))

  messaggio ={"primoNumero": primoNumero,
               "operazione": operazione,
               "secondoNumero": secondoNumero
              }
  messaggio=json.dumps(messaggio)
  

  #Ricezione dal server 
  sock.sendto(messaggio.encode("UTF-8"),(SERVER_IP,SERVER_PORT))
  print(f"Messaggio inviato al server")
  
  data,addr=sock.recvfrom(BUFFER_SIZE)
  print(f"Messaggio ricevuto dal server: {data.decode()}")


sock.close()
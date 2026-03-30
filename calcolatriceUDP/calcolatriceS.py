import socket, json

SERVER_IP="127.0.0.1"
SERVER_PORT=5005
BUFFER_SIZE=1024

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((SERVER_IP,SERVER_PORT))

print(f"Server in attesa di calcolare...")

while True:
      data,addr=sock.recvfrom(BUFFER_SIZE)
      print(f"Ricevuto messaggio da {addr}: {data.decode()}")

      if not data:
            break
      data=data.decode()

      data=json.loads(data)
      primoNumero=float(data["primoNumero"])
      operazione=data["operazione"]
      secondoNumero=float(data["secondoNumero"])

      reply=""
      if operazione=="+":
            reply=str(primoNumero+secondoNumero)
      elif operazione=="-":
            reply=str(primoNumero-secondoNumero)
      elif operazione=="*":    
            reply=str(primoNumero*secondoNumero)
      elif operazione=="/":
            reply=str(primoNumero/secondoNumero)

      sock.sendto(reply.encode(),addr)
import socket
import threading

HOST_IP = "127.0.0.1"
PORT = 65266

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST_IP,PORT))

clients = []
server.listen()
print("Waiting for connection")

def handleClient(client):
    try:
        while True:
            message = client.recv(4096)
            if message:
                str = f"{message.decode()}"
                for i in clients:
                    i.send(str.encode("utf-8"))
                print(str)
    except:
        clients.remove(client)
        client.close()

while True:
    try:
        client, address = server.accept()
        print("Connected by", address)
        clients.append(client)

        thread = threading.Thread(target=handleClient, args=(client,), daemon=True)
        thread.start()
    except:
        for client in clients:
            client.close()
        break
    # handleClient(client)

import socket
import threading

HOST_IP = "127.0.0.1"
PORT = 65266

def receiveResponses(socket):
    while True:
        try:
            data = client_socket.recv(4096)
            if data:
                print(data.decode("utf-8"))
        except:
            socket.close()

all_messages = []
username = "Dima"
message = f"{username}: Hi"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST_IP, PORT))

thread = threading.Thread(target=receiveResponses, args=(client_socket,), daemon=True)
thread.start()

running = True

while running:
    message = input(">")
    if message == "exit":
        running = False
    message = f"{username}: {message}"
    client_socket.send(message.encode("utf-8"))

# client_socket.send(message.encode("utf-8"))
# message = client_socket.recv(4096)
# print(message)

# client_socket.send(b"Hello World")

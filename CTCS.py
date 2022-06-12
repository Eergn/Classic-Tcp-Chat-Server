import threading
import socket

ServerHost = "127.0.0.1"
Port = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ServerHost, Port))
server.listen()

clients = []
usernames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} left the chat'.encode('ascii'))
            usernames.remove(username)
            break


def receive():
    print("The Server Is Listening")
    while True:
        client, address = server.accept()
        print(f"{str(address)}Connected")
        client.send("Username? >> ".encode("ascii"))
        try:
            username = client.recv(1024).decode('ascii')
        except:
            username = "Guest User"
        usernames.append(username)
        clients.append(client)
        print(f"User Name Is {username}")
        broadcast((username + " Joined The Chat! .\n").encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()

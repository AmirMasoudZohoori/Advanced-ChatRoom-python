from socket import *
from threading import Thread


server_port = 1830
config_server = ('', server_port)


server_socket = socket(AF_INET, SOCK_STREAM)

server_socket.bind(config_server)
server_socket.listen()

clients = []
clients_name = []


def broadcast_message(message, c=None):
    for client in clients:
        if client is not c:
            client.send(message.encode())


def get_message(client):
    while True:
        try:
            smg = message = client.recv(1024).decode()
            print(message)

            if smg.startswith('KICK'):
                if clients_name[clients.index(client)] == 'admin':
                    Kick_client(smg[5:])

                else:
                    client.send(
                        "command refuse , this commad for admin server ...".encode())

            elif smg.startswith("BAN"):
                if clients_name[clients.index(client)] == 'admin':
                    Band_client(smg[4:])

                else:
                    client.send(
                        "command refuse , this commad for admin server ...".encode())

            else:
                broadcast_message(message, client)

        except:
            if client in clients:
                index = clients.index(client)
                client.close()
                clients.remove(client)
                name = clients_name[index]
                clients_name.remove(name)
                break


def join_client():
    while True:

        client, info_client = server_socket.accept()
        print(f"the clinet {info_client} join in server chat")

        client.send("102457854210".encode())
        name = client.recv(1024).decode().strip()

        if name.strip().__eq__("admin"):
            client.send('1021212454'.encode())
            password = client.recv(1024).decode()
            if password != "123":
                client.send("Refuse".encode())
                client.close()
                continue

        with open('ban.txt', 'r') as ban_file:
            bans = ban_file.readlines()

        if name+'\n' in bans:
            client.send("you are ban from server ...".encode())
            client.close()
            continue

        clients_name.append(name)
        print(f"{name} join to chat ")
        clients.append(client)
        client.send("connected to chat ...".encode())
        thread = Thread(target=get_message, args=(client, ))
        thread.start()


def Kick_client(name):
    if name in clients_name:
        name_index = clients_name.index(name)
        clients_name.remove(name)
        client = clients[name_index]
        client.send("Kick785".encode())
        clients.remove(client)
        client.close()
        broadcast_message(f'{name} Kick from chat by admin ...')


def Band_client(name):
    if name in clients_name:
        with open('ban.txt', 'a') as ban_file:
            ban_file.write(f'{name}\n')

        name_index = clients_name.index(name)
        clients_name.remove(name)
        client = clients[name_index]
        client.send("ban785".encode())
        clients.remove(client)
        client.close()
        broadcast_message(f'{name} Ban from server ...')


if __name__ == "__main__":
    while True:
        try:
            with open('ban.txt', 'a') as f:
                pass
            print("server start ...")
            join_client()
        except:
            print("connection loss ...")

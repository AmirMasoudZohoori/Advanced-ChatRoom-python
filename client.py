from socket import *
from threading import Thread

server_info = ("194.5.188.46", 1830)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(server_info)
name = input("Enter Your Name : ")
if name == 'admin':
    password = input("Enter admin password : ")
stop_thread = False


def get_message():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            massage = client_socket.recv(1024).decode()
            if massage == "102457854210":
                client_socket.send(name.encode())

            elif massage == "1021212454":
                client_socket.send(password.encode())

            elif massage == "Refuse":
                print("Connection was Refused ! wrong password")
                client_socket.close()
                stop_thread = True

            elif massage == "Kick785":
                print("you kick from chat ...")
                client_socket.close()
                stop_thread = True

            elif massage == "ban785":
                print("you ban from server ...")
                client_socket.close()
                stop_thread = True

            elif massage != '':
                print(massage)

        except:
            client_socket.close()
            stop_thread = True
            break


def send_massage():
    while True:
        if stop_thread:
            break

        c = input("")
        message = f'{name} :{c}'

        if message[len(name)+2:].startswith('/'):
            if name == "admin":

                if message[len(name)+2:].startswith('/Kick'):

                    client_socket.send(
                        f'KICK {message[len(name)+2+6:]}'.encode())
                    print("send commad ...")

                elif message[len(name)+2:].startswith('/Ban'):

                    client_socket.send(
                        f'BAN {message[len(name)+2+5:]}'.encode())
                    print("send commad ...")

        else:
            client_socket.send(message.encode())


send = Thread(target=send_massage)
get = Thread(target=get_message)

get.start()
send.start()

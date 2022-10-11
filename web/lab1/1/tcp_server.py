import threading
import socket
from datetime import datetime
import time

host = "127.0.0.1"
port = 8889

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('ascii'))

        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        print(f'{nickname} has just join the chat!')

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def handle(client):
    while True:
        index = clients.index(client)
        nickname = nicknames[index]

        try:
            message = client.recv(1024)

            if message.decode('ascii') == "quit":
                raise Exception

            print(message.decode('ascii'), " -- at ", datetime.now().strftime("%H:%M:%S"))
            time.sleep(5)
            sent_data_len = client.send((message.decode('ascii') + " -- at " + datetime.now().strftime("%H:%M:%S")).encode('ascii'))
            if sent_data_len == len(message):
                print("Data size is correct")
            else:
                print("Data size is not correct")
            # broadcast(message)
        except:
            clients.remove(client)
            client.close()

            print(f'{nickname} left the chat')

            nicknames.remove(nickname)
            break

print('Server is listening...')

receive()



#
# import socket
#
#
# server = socket.socket()
# name = input("Your name : ")
#
# server.connect(("127.0.0.1", 8000))
# server.send(name.encode())
# socket_name = server.recv(1024)
# server_name = socket_name.decode()
#



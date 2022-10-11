import threading
import socket


nickname = input('Choose a nickname : ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8889))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            client.close()
            break


def write():
    while True:
        message = input()
        client.send(message.encode('ascii'))
        if message == "quit":
            client.close()


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()


















# import socket
#
# my_socket = socket.socket()
# my_socket.bind(("127.0.0.1", 8000))
# my_socket.listen()
#
# print("Server start")
# name=input("name : ")
# conn, add = my_socket.accept()
#
# client = (conn.recv(1024)).decode()
# print(client + " log in")
# conn.send(name.encode())
#
# while True:
#     msg = input("You : ")
#     conn.send(msg.encode())
#     msg = conn.recv(1024)
#     msg = msg.decode()
#     print(client, " : ", msg)

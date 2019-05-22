#多用户接入聊天
import socket
import threading


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8888))
server.listen()

def handle_socket(socket, address):
    while True:
        data = socket.recv(1024)
        print(data.decode('utf8'))
        re_data = input()
        socket.send(re_data.encode('utf8'))

while True:
    sock, addr = server.accept()
    
    #每有一个新的连接就开一个新的线程
    client_thread = threading.Thread(target=handle_socket, 
                                     args=(sock, addr))
    
    client_thread.start()




    #启动socket_server3.py
    #启动两个socket_client2.py


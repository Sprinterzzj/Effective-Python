#单对单聊天
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8888))
server.listen()
#阻塞直到有client链接进来, 进入while循环
sock, addr = server.accept()

while True:
    data = sock.recv(1024)
    print(data.decode('utf8'))

    #终端输入数据
    re_data = input()
    sock.send(re_data.encode('utf8'))
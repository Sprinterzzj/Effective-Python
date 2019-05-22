#socket_client.py
import socket

#1.初始化 socket server实例
client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

#2.链接
client.connect(('127.0.0.1', 8888))

#3.发送/接收数据
client.send('bobby'.encode('utf8'))
data = client.recv(1024)
print(data.decode('utf8'))
client.send('mooc'.encode('utf8'))

#4.如果不用了就关闭
client.close()
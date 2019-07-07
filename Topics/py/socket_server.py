#socket_sever.py
import socket

#1.初始化 socket server实例
#family: ipv4, type: TCP 
sever = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

#2. 绑定地址和端口
sever.bind(('0.0.0.0', 8888))

#3. 开始监听
sever.listen()

#4. accept, 阻塞等待链接请求
sock, addr = sever.accept()

print(addr)

#5. 获取从客户端发送的数据, 假设一次获取1024字节的数据
data = sock.recv(1024)
print(data.decode('utf8'))
sock.send('hello'.encode('utf8'))
data = sock.recv(1024)
print(data.decode('utf8'))
#6.如果不用了就关闭
sock.close()

#7.一般来讲我们不会关闭sever
sever.close()
import socket
from urllib.parse import urlparse

def get_url(url):
    #通过socket而不是requests/urlib来请求html
    url = urlparse(url)
    client = socket.socket(socket.AF_INFT, socket.SOCK_STREAM）
    #提取主域名
    host = url.netloc
    path = url.path
    if path == '':
        path = '/'
    client.connect((host, 8888))

    #下面来模拟发送http请求
    client.send('GET {}\r\n')



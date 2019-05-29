import socket
from urllib.parse import urlparse

def get_url(url):
    #通过socket而不是requests/urlib来请求html
    url = urlparse(url)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #提取主域名
    host = url.netloc
    path = url.path
    if path == '':
        path = '/'
    client.connect((host, 80))

    #下面来模拟发送http请求
    client.send(
        'GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n'.\
            format(path, host).encode('utf8')
            )
    
    data = b''
    while True:
        d = client.recv(1024)
        if d:
            data += d
        else:
            break
    data = data.decode('utf8')
    #去掉开头那些部分
    html_data = data.split('\r\n\r\n')[1]
    print(html_data)
    client.close()

if __name__ == "__main__":
    get_url('http://baidu.com')



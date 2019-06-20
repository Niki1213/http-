"""
部分主程序
"""
from socket import *
from threading import Thread
from config import *
import re, json


# env:{'method': 'GET', 'info': '/'}
def connect_frame(env):
    """

    :param env: 得到要发送给frame的请求字典
    :return: 　从frame得到的数据
    """
    # 建立socket客户端
    sockfd = socket()
    try:
        sockfd.connect((frame_ip, frame_port))
    except Exception as e:
        print(e)
        return
    # 将env转换为json
    data = json.dumps(env)
    sockfd.send(data.encode())
    # 从frame接收返回数据
    data = sockfd.recv(1024 * 1024).decode()
    return json.loads(data)  # 字典

    # 实现http功能


class HttpServer:
    def __init__(self):
        self.address = ADDR
        self.create_socket()
        self.bind()

    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)

    # 绑定地址
    def bind(self):
        self.sockfd.bind(self.address)
        self.ip = self.address[0]
        self.port = self.address[1]

    # 启动服务
    def serve_forever(self):
        self.sockfd.listen(3)
        print("创建监听套接字端口　%d" % self.port)
        while True:
            connfd, addr = self.sockfd.accept()
            print("连接", addr)
            client = Thread(target=self.handle, args=(connfd,))
            client.setDaemon(True)
            client.start()

    # 处理浏览器请求
    def handle(self, connfd):
        request = connfd.recv(4096).decode()
        # print(request)
        pattern = r"(?P<method>[A-Z]+)\s+(?P<info>/\S*)"
        try:
            env = re.match(pattern, request).groupdict()
        except:
            connfd.close()
            return
        else:
            # print(env)
            # data {status: '200', data: 'ccccc'}
            data = connect_frame(env)  # 用户与frame交互
            if data:
                print(data)
                self.response(connfd, data)

    # 将data组织为response发送给浏览器
    def response(self, confd, data):
        if data['status'] == "200":
            responseHeaders = "HTTP/1.1 200 OK\r\n"
            responseHeaders += "Content-Type:text/html\r\n\r\n"
            responseBoy = data["data"]
        elif data["status"] == "404":
            responseHeaders = "HTTP/1.1 404 Not Fount\r\n"
            responseHeaders += "Content-Type:text/html\r\n\r\n"
            responseBoy = data["data"]
        elif data["status"] == "500":
            pass
        # 将数据发送
        response = responseHeaders + responseBoy
        confd.send(response.encode())


httpd = HttpServer()
httpd.serve_forever()

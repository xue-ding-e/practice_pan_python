import socket
from pan.config import settings


class Server(object):
    def __init__(self):
        self.host = settings.HOST
        self.port = settings.PORT

    def run(self, handler_class):
        # socket服务端
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(5)

        while True:
            conn, addr = sock.accept()
            print("新客户来连接")
            # 新客户到来。 PhaHandler对象
            instance = handler_class(conn)
            # 处理客户端的请求。PanHandler对象.execute
            while True:
                result = instance.excute()
                if not result:
                    break
            conn.close()
        sock.close()
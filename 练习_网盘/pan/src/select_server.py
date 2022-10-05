import socket
import select
from pan.config import settings

class SelectServer(object):
    '''  基于IO多路复用的socket的服务端口  '''

    def __init__(self):
        self.host = settings.HOST
        self.port = settings.PORT
        self.socket_object_list = []
        self.conn_handler_map = {}

    def run(self, handler_class):   # handler_class = PanHandler
        server_ob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_ob.setsockopt(socket.SOL_SOCKET, socket.SOCK_STREAM, 1)

        # 非阻塞
        server_ob.setblocking(True)

        server_ob.bind((self.host, self.port))  # 有两个括号
        server_ob.listen(5)

        self.socket_object_list.append(server_ob)

        while True:
            r, w, e = select.select(self.socket_object_list, [], [], 0.05)

            for sock in r:
                # sock = "客户端socket对象4“

                # 新连接到来，执行handler的__init__方法
                if sock == server_ob:
                    print("新客户端来连接")
                    conn, addr = server_ob.accept()
                    self.socket_object_list.append(conn)
                    # 实例化handler类，即：类(conn)
                    """
                    conn_handler_map = {
                        "客户端socket对象1": PanHander(conn1),
                        "客户端socket对象2": PanHander(conn2)
                        }
                    """
                    self.conn_handler_map[conn] = handler_class(conn)
                    continue
                # 一旦有请求发来，找到相关的 handler 对象， 执行他的 execute方法
                # execute方法返回False, 则意味着此客户端要断开连接

                handler_object = self.conn_handler_map[sock]

                # 找到execute去处理各自的业务逻辑
                result = handler_object.execute()   # 执行PanHandler.execute()
                if not result:
                    self.socket_object_list.remove(sock)
                    del self.conn_handler_map[sock]
        sock.close()
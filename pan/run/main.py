from pan.src.pan import PanHandler
from pan.src.server import Server
from pan.src.select_server import SelectServer

if __name__ == '__main__':
    # 执行server服务端或者IO多路复用服务端
    # server = Server()
    server = SelectServer()
    server.run(PanHandler)




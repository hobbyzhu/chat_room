from common.config import *
import socket


class ServerSocket(socket.socket):
    """
    初始化服务器，对服务器的的设置
    """

    def __init__(self):
        # 设置为tcp类型
        # super(ServerSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM) # python2.x版本用法
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定地址和端口
        self.bind((SERVER_IP, SERVER_PORT))

        # 监听模式
        self.listen(SERVER_NUMBER)

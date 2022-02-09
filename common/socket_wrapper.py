class Socket_Wrapper(object):
    """
    套接字包装模块
    """

    def __init__(self, sock):
        self.sock = sock

    def recv_date(self):
        """
        接受数据并解码
        """
        try:
            return self.sock.recv(512).decode('utf-8')
        except:
            return ''

    def send_date(self, massage):
        """

        :param massage:
        :return: 有返回值 ，显示发送了多少数据
        """
        return self.sock.send(massage.encode('utf-8'))

    def close_socket(self):
        """
        关闭套接字
        """
        self.sock.close()

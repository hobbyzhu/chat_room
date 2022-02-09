import socket


def test():
    # 测试客户端
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(('127.0.0.1', 6666))


    while True:
        info = input('请输入->')
        soc.send(info.encode('utf-8'))
        recv_date = soc.recv(1024)
        print(recv_date.decode('utf-8'))
    soc.close()



if __name__ == '__main__':
    test()

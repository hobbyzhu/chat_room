from common.server_socket import ServerSocket
from common.socket_wrapper import Socket_Wrapper
import threading
from common.config import *
from common.response_protocol import Response_Protocol
from model.db_sql import DB


class Server(object):
    """
    服务器核心类
    """

    def __init__(self):
        # 创建服务器套节字
        self.server_socket = ServerSocket()

        # 创建请求的ID和方法的关联关系 ，不需要在子线程中名称调用。
        self.request_handle_function = {}
        self.register(Request_Login, self.request_login_handle)  # 调用register封装
        self.request_handle_function[Request_Chat] = self.request_chat_handle  # 没有调用

        # 创建保存当前登录用户信息
        self.clients = {}

        # 创建数据库管理对象
        self.db = DB()

    def register(self, request_id, handle_function):
        """
        将重复调用进行简单封装
        :param request_id:  函数id
        :param handle_function: 执行函数
        :return: None
        """
        self.request_handle_function[request_id] = handle_function

    def start_up(self):
        """
        获取客户端连接，并提供服务，服务器收发消息的的编码和解码被封装在common.socket_wrapper中
        """
        while True:
            print('正在获取客户端连接')
            # 获取客户端连接
            soc, addr = self.server_socket.accept()
            print('获取到客户端{0}'.format(addr))

            # 创建收发对象
            client_soc = Socket_Wrapper(soc)

            # 创建子线程，用于收发数据
            # t = threading.Thread(target=self.request_handle, args=(client_soc,))
            # t.start()
            threading.Thread(target=lambda: self.request_handle(client_soc, addr)).start()

    # 定义函数，并被用于多线程
    def request_handle(self, client_soc, addr):
        while True:
            # 接受客户端数据
            recv_date = client_soc.recv_date()

            # 如果没有数据表示为断开连接
            if not recv_date:
                # 关闭客户端，移除用户
                self.remove_offline_user(client_soc, addr)
                client_soc.close_socket()
                break

            # 解析数据
            parse_date = self.parse_request_test(recv_date)

            # 分析请求类型，并调用函数 ex{'request_id': '0001', 'username': '11', 'password': '1'}
            print('收到一条数据内容>>{0}'.format(parse_date))

            # 判断类型，调用函数   功能重构，高可用性 和下面相同的原理，get放弃不存在的key
            handle_function = self.request_handle_function.get(parse_date['request_id'])
            if handle_function:
                handle_function(client_soc, parse_date)

            # 功能重构，高可用性 和上面相同的原理
            # if parse_date['request_id'] == Request_Login:
            #     self.request_login_handle()
            # elif parse_date['request_id'] == Request_Chat:
            #     self.request_chat_handle()

    def remove_offline_user(self, client_soc, addr):
        """
        客户端下线处理,将下线用户从字典中移除
        """
        print('开始用户离线{0}'.format(addr))
        for username, info in self.clients.items():
            if info['sock'] == client_soc:
                print(1, self.clients)
                del self.clients[username]
                print(2, self.clients)
                break

    def parse_request_test(self, text):
        """
        解析客户端发来的数据,并未对数据进行处理，只是判断数据的类型
        用户登录：0001|username|password
        聊天消息：0002|username|massages
        """
        request_list = text.split('|')
        request_date = {}
        request_date['request_id'] = request_list[0]
        if request_date['request_id'] == Request_Login:
            # 用户请求登录
            request_date['username'] = request_list[1]
            request_date['password'] = request_list[2]


        elif request_date['request_id'] == Request_Chat:
            # 用户聊天消息
            request_date['username'] = request_list[1]
            request_date['massages'] = request_list[2]

        return request_date

    def request_login_handle(self, client_soc, parse_date):
        """
        收到登录请求
        :return:
        """
        print('收到登录请求')
        # 获取账号密码
        username = parse_date['username']
        password = parse_date['password']

        # 检查能否登录
        res, nickname, username = self.check_user_login(username, password)

        # 登录成功，保存在线用户信息
        if res == str(1):
            self.clients[username] = {'sock': client_soc, 'nickname': nickname}

        # 拼接客户端响应，并发送
        response_test = Response_Protocol.response_login_result(res, nickname, username)
        client_soc.send_date(response_test)

    def request_chat_handle(self, client_soc, parse_date):
        """
        收到聊天请求,并转发到各在线客户端
        :param client_soc: 发送消息的客户端对象
        :param parse_date: 客户端发送的消息，字典
        :return:
        """
        print('收到聊天请求', client_soc, parse_date)

        username = parse_date['username']
        massages = parse_date['massages']

        # 登录用户,已经登录用户信息在字典中，通过username获取nickname
        nickname = self.clients[username]['nickname']

        # 拼接消息
        mas = Response_Protocol.response_chat(nickname=nickname, message=massages)

        # 并转发给用户，字典sock key是发送对象
        for U_name, info in self.clients.items():
            if username == U_name:  # 发送者本人不需要接受消息
                continue
            info['sock'].send_date(mas)

    def check_user_login(self, username, password):
        """
        检查用户用户是否正确输入
        :param username:前端输入
        :param password:前端输入
        :return: 返回结果 0 fail 1 success
        不要提示用户是密码错误还是用户名错误，减少风险
        """
        # 数据库查询用户信息
        result = self.db.get_user_one(f"select * from users WHERE user_name ='{username}'")

        # 用户名密码匹配情况
        if not result:
            return '0', '', username
        if password != result['user_password']:
            return '0', 'None', username
        return '1', result['user_nickname'], username


if __name__ == "__main__":
    Server().start_up()

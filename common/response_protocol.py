from common.config import *


class Response_Protocol(object):
    """
    响应拼接
    """

    @staticmethod  # 静态方法，简单拼接字符串
    def response_login_result(result, nickname, username):
        """
        响应登录拼接 数据格式：'响应协议编号|登录结果|用户昵称|用户名'
        result ： 登录结果 0 表示失败 1 表示成功
        nickname： 用户昵称，登录失败为空
        username： 用户名 ，登录失败为空
        result ： 返回结果为str类型
        """
        return Delimiter.join([Response_Login_Result, result, nickname, username])

    @staticmethod  # 静态方法，简单拼接字符串
    def response_chat(nickname, message):
        """
        响应聊天拼接 数据格式：'响应协议编号|聊天发送者昵称|聊天内容'
        nickname ：发送人
        massage： 聊天内容
        result ： 返回结果为str类型
        """
        return Delimiter.join([Response_Chat, nickname, message])

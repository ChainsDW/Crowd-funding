import hashlib
import time
import random
import collections
import smtplib
from email.mime.text import MIMEText



Email = 'smtp.126.com'
Username = 'l345323642'
Password = 'l94355'
mail_postfix = '126.com'


class StatusCodeEnum:

    Failed = 1000
    AuthFailed = 1001
    ArgsError = 1002
    Success = 2000


class BaseResponse:

    def __init__(self):
        self.status = False
        self.code = StatusCodeEnum.Success
        self.data = None
        self.summary = None
        self.message = {}


def random_code():
    code = ''
    for i in range(4):
        current = random.randrange(0,4)
        if current != i:
            temp = chr(random.randint(65,90))
        else:
            temp = random.randint(0,9)
        code += str(temp)
    return code


def generate_md5(value):
    r = str(time.time())
    obj = hashlib.md5(r.encode('utf-8'))
    obj.update(value.encode('utf-8'))
    return obj.hexdigest()



def tree_search(d_dic, comment_obj):
    # 在comment_dic中一个一个的寻找其回复的评论
    # 检查当前评论的 reply_id 和 comment_dic中已有评论的nid是否相同，
    #   如果相同，表示就是回复的此信息
    #   如果不同，则需要去 comment_dic 的所有子元素中寻找，一直找，如果一系列中未找，则继续向下找
    for k, v_dic in d_dic.items():
        # 找回复的评论，将自己添加到其对应的字典中，例如： {评论一： {回复一：{},回复二：{}}}
        if k[0] == comment_obj[2]:
            d_dic[k][comment_obj] = collections.OrderedDict()
            return
        else:
            # 在当前第一个跟元素中递归的去寻找父亲
            tree_search(d_dic[k], comment_obj)


def build_tree(comment_list):

    comment_dic = collections.OrderedDict()

    for comment_obj in comment_list:
        if comment_obj[2] is None:
            # 如果是根评论，添加到comment_dic[评论对象] ＝ {}
            comment_dic[comment_obj] = collections.OrderedDict()
        else:
            # 如果是回复的评论，则需要在 comment_dic 中找到其回复的评论
            tree_search(comment_dic, comment_obj)
    return comment_dic


def send_mail(reciever, content, type=False, pro_name=None):
    """
    :param reciever: 收件人
    :param content: 验证码
    :return:
    发验证码邮件
    """
    me="窝头"+"<"+Username+"@"+mail_postfix+">"
    if type:
        message = '【窝头科技】您'+pro_name+'的文件下载密钥为：' + content + '。请务必保存好您的密钥，否则文件资料将丢失。'
    else:
        message = '【窝头科技】您的验证码为：'+content+'。'
    msg = MIMEText(message,_subtype='plain')
    if type:
        msg['Subject'] = '密钥'
    else:
        msg['Subject'] = '验证码'
    msg['From'] = me
    msg['To'] = reciever               #将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(Email)                            #连接服务器
        server.login(Username,Password)               #登录操作
        server.sendmail(me, reciever, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(str(e))
        return False


if __name__ == '__main__':
    send_mail('751009167@qq.com', '0928')
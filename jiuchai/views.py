from django.shortcuts import render, HttpResponse, redirect
from django.http import StreamingHttpResponse
from jiuchai.utils import utils, auto_get_data, forms
from jiuchai.utils.blockchain import *
import json
from jiuchai import models
from xuejieBT.settings import BASE_DIR
import os
from django.core.paginator import Paginator
from django.contrib.auth import login,authenticate,logout
from jiuchai.utils import utilsb
from django.utils import timezone as datetime
from datetime import date
import time
# Create your views here.

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


def is_login(func):
    def inner(request):
        print(request.session.get('is_login'))
        if request.session.get('is_login') and request.session.get('role') == 'user':
            return func(request)
        else:
            return redirect('/login.html')
    return inner


def index(request):
    return render(request, 'jiuchai/index.html')


# def view_traslations(request):
#     # block = view_chain()
#     print(block)
#     print(block['chain'][0]['timestamp'])
#     return render(request, 'blockchains.html', {'block': block})

@is_login
def mine(request):
    responese = utils.mine()
    return render(request, 'jiuchai/created_tran.html')


@is_login
def create_transaction(request):
    #创建交易
    if request.method == 'POST':
        values = {}
        values['sender'] = request.session.get('username')
        values['recipient'] = request.POST.get('recipient')
        values['amount'] = int(request.POST.get('amount'))
        project = models.Projects.objects.get(name=request.POST.get('project_name'))
        values['companyID'] = int(project.id)
        if request.POST.get('c') == 'pr':
            values['status'] = 'promise'
        else:
            values['status'] = 'true_trans'
        values['stage'] = request.POST.get('stage')
        utils.new_transaction(values)
        utils.mine()
        utils.verify_chain()
        return HttpResponse('OK')
    project_id = request.GET.get('pr')
    project = models.Projects.objects.get(id=project_id)
    return render(request, 'jiuchai/created_tran.html', {'project': project})


def view_chain(request):
    #查看区块
    chain = utils.full_chain()
    print(chain)
    project_id = request.GET.get('pr')

    return render(request, 'jiuchai/blockchains.html', {'blocks': chain})


def view_trans(request):
    #查看区块交易
    index = int(request.GET.get('index')) - 1
    chain = utils.full_chain()
    return render(request, 'jiuchai/blocktrans.html', {'trans': chain['chain'][index]['transactions']})


@is_login
def register_nodes(request):
    values = request.POST
    response = utils.register_nodes(values)
    return render(request, 'jiuchai/created_tran.html')


@is_login
def consensus(request):
    response = utils.consensus()
    return render(request, 'jiuchai/created_tran.html')

def indexs(request):
    return render(request, 'jiuchai/index.html')


@is_login
def post_data(request):
    #发起众筹项目
    data = utilsb.BaseResponse()
    if request.method == "POST":
        sender = request.POST.get('sender')
        if sender != request.session.get('username'):
            data.summary = '发起人必须为本人'
            return render(request, 'jiuchai/post_data.html', {'data': data})
        name = request.POST.get('name')
        amount_goal = int(request.POST.get('amount_goal'))
        time_limit = request.POST.get('time_limit')
        brief = request.POST.get('brief')
        file = request.FILES.get('myfile')
        phone_number = request.POST.get('phone_number')
        goal = request.POST.get('goal')
        returns = request.POST.get('return')
        if file:
            file_adr = os.path.join(BASE_DIR, 'file_pag', name)
            os.mkdir(file_adr)
            file_addr = os.path.join(name, file.name)
            with open(os.path.join(file_adr, file.name), 'wb') as f:
                f.write(file.read())
        else:
            file_addr = None
        models.Projects.objects.create(name=name,
                                       sender=sender,
                                       phone_number=phone_number,
                                       amount_goal=amount_goal,
                                       time_limit=time_limit,
                                       brief=brief,
                                       file_adr=file_addr,
                                       award=returns,
                                       goal=goal,
                                       status=0)
        companyID = models.Projects.objects.get(name=name,sender=sender).id
        return redirect('/homepage')
    data.data = request.session.get('username')
    return render(request, 'jiuchai/post_data.html',{'data': data})


def index_jiucai(request):
    #项目详情
    if request.method == 'POST':
        key = request.POST.get('key')
        pro_name = request.POST.get('path').split('\\')[0]
        project_id = models.Projects.objects.get(name=pro_name).id
        dic = auto_get_data.find_prove_dic(project_id)
        utils.dic_to_file(key, dic, pro_name)
        return HttpResponse(json.dumps({'status':True}))
    datas = {'status': False, 'count': 0}
    project_id = request.GET.get('pr')
    datas['count'] = auto_get_data.count_project_amount(project_id)
    if project_id:
        project = models.Projects.objects.get(id=project_id)
    else:
        return redirect('homepage')

    if datas['count'] >= project.amount_goal:
        datas['status'] = True
    return render(request, 'jiuchai/jiucai.html', {'project': project, 'datas': datas})


def homepage(request):
    #主页
    utils.consensus()
    page = request.GET.get('page')
    if not page:
        page = 1
    projects = models.Projects.objects.filter(status=2).order_by('id').all()
    p = Paginator(projects, 2)
    project = p.page(page)
    return render(request, 'jiuchai/homepage.html', {'projects':project})


def project_brief(request):
    #返回项目简介（废弃）
    project_id = request.GET.get('pr')
    if project_id:
        project = models.Projects.objects.get(id=project_id)
    else:
        return redirect('homepage')
    return render(request, 'jiuchai/brief.html', {'project': project})


@is_login
def download(request):
    #下载项目附件
    path = request.GET.get('path')
    file_name = path.split('\\')[1]
    response = StreamingHttpResponse(utils.file_iter(path, 512))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response


def project_trans(request):
    """
    单个项目的所有交易
    """
    index = request.GET.get('pr')
    project_name = models.Projects.objects.get(id=index).name
    return render(request, 'jiuchai/project_tran.html', {'index': index, 'name': project_name})


def acc_login(request):
    """
    :param request:
    :return:
    登陆
    """
    rep = utilsb.BaseResponse()
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            obj = models.UserAccount.objects.filter(email=email,
                                                    password=form.cleaned_data.get('pwd'))
            if obj:
                request.session['is_login'] = True
                request.session['username'] = email##session邮箱
                request.session['role'] = 'user'
                rep.status = True
            else:
                rep.summary = '邮箱错误或密码错误'
        else:
            rep.summary = '邮箱非法'
        return HttpResponse(json.dumps(rep.__dict__))
    return render(request, "jiuchai/login.html")


def acc_logout(request):

    logout(request)

    return redirect("/account/login/")


def send_msg(request):
    """
    注册时，发送邮箱验证码
    :param request:
    :return:
    """
    rep = utilsb.BaseResponse()
    form = forms.SendMsgForm(request.POST)
    if form.is_valid():
        _value_dict = form.clean()
        email = _value_dict['email']

        has_exists_email = models.UserInfo.objects.filter(email=email).count()

        if has_exists_email:
            rep.summary = "此邮箱已经被注册"
            return HttpResponse(json.dumps(rep.__dict__))

        current_date = datetime.datetime.now()
        code = utilsb.random_code()
        count = models.SendMsg.objects.filter(email=email).count()
        if not count:
            models.SendMsg.objects.create(code=code, email=email, ctime=current_date)
            rep.status = True
        else:
            limit_day = current_date - datetime.timedelta(hours=1)

            times = models.SendMsg.objects.filter(email=email, ctime__gt=limit_day, times__gt=9).count()
            if times:
                rep.summary = "'已超最大次数（1小时后重试）'"
            else:
                unfreeze = models.SendMsg.objects.filter(email=email, ctime__lt=limit_day).count()
                if unfreeze:
                    models.SendMsg.objects.filter(email=email).update(times=0)

                from django.db.models import F

                obj = models.SendMsg.objects.filter(email=email).update(code=code,
                                                                  ctime=current_date,
                                                                  times=F('times') + 1)

                utilsb.send_mail(email, code)
                rep.status = True
    else:
        rep.summary = form.errors['email'][0]
    return HttpResponse(json.dumps(rep.__dict__))


def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method == 'POST':
        rep = utilsb.BaseResponse()
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            current_date = datetime.datetime.now()
            limit_day = current_date - datetime.timedelta(minutes=1)
            _value_dict = form.clean()
            is_valid_code = models.SendMsg.objects.filter(email=_value_dict['email'],
                                                          code=request.POST.get('email_code'),
                                                          ctime__gt=limit_day).count()
            if not is_valid_code:
                rep.message['email_code'] = [{'message': '邮箱验证码不正确'}]
                return HttpResponse(json.dumps(rep.__dict__))

            has_exists_email = models.UserInfo.objects.filter(email=_value_dict['email']).count()

            if has_exists_email:
                rep.message['email'] = [{'message': '邮箱已经存在'}]
                return HttpResponse(json.dumps(rep.__dict__))

            has_exists_username = models.UserInfo.objects.filter(name=request.POST.get('name')).count()
            if has_exists_username:
                rep.message['username'] = [{'message': '用户名已经存在'}]
                return HttpResponse(json.dumps(rep.__dict__))

            form.save()
            # 当前用户的所有信息
            role = models.Role.objects.get(name=request.POST.get('role'))
            obj = models.UserAccount.objects.create(username=request.POST.get('username'),
                                                    email=_value_dict['email'],
                                                    password=request.POST.get('password'),
                                                    user_info_id=5)
            obj.role.add(role)
            obj.save()

            user_info_dict = {'email': obj.email, 'username': obj.username}

            models.SendMsg.objects.filter(email=_value_dict['email']).delete()

            request.session['is_login'] = True
            request.session['user_info'] = user_info_dict
            rep.status = True
        else:
            error_msg = form.errors.as_json()
            rep.message = json.loads(error_msg)
        return HttpResponse(json.dumps(rep.__dict__))
    return render(request, 'jiuchai/register.html')


def download_chain(request):
    # 下载项目附件
    path = request.GET.get('path')
    file_name = path.split('\\')[1]
    response = StreamingHttpResponse(utils.file_iter(path, 512))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response


@is_login
def myCrowdfunding(request):
    email = request.session.get('username')
    username = models.UserAccount.objects.get(email=email).username
    return render(request, 'jiuchai/myCrowdfunding.html', {'username': username})


@is_login
def get_user_data(request):
    data = {'status': False, 'data': [], 'error': None}
    if request.POST.get('type') == 'support':
        email = request.session.get('username')
        types = request.POST.get('conditions')
        data_dict = auto_get_data.find_user_project(email, types)
        if len(data_dict) != 0:
            data['status'] = True
            for project_id, amount in data_dict.items():
                project = models.Projects.objects.get(id=project_id)
                count = auto_get_data.count_project_amount(project_id)
                days = (project.time_limit - date.today()).days
                if days <= 0:
                    days = '已过期'
                project_dic = {'id': project.id, 'name': project.name,'goal':project.amount_goal, 'counts': count, 'days': days, 'amount': amount}
                data['data'].append(project_dic)
        return HttpResponse(json.dumps(data))
    elif request.POST.get('type') == 'funding':
        email = request.session.get('username')
        projects = models.Projects.objects.filter(sender=email)
        if projects:
            data['status'] = True
            for project in projects:
                project_dic = project.__dict__
                del project_dic['_state']
                project_dic['time_limit'] = datetime.datetime.strftime(project_dic['time_limit'], "%Y-%m-%d")
                data['data'].append(project_dic)
        return HttpResponse(json.dumps(data))

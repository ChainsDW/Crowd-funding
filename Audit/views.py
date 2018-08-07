from django.shortcuts import render, redirect, HttpResponse
from Audit import models
from jiuchai.models import Projects,UserInfo
import json
from jiuchai.utils import utils, utilsb
from xuejieBT.settings import BASE_DIR
import os
from django.http import StreamingHttpResponse
import shutil
# Create your views here.


def is_login(func):
    def inner(request):
        print(request.session.get('is_login'))
        if request.session.get('is_login') and request.session.get('role') == 'audit':
            return func(request)
        else:
            return redirect('/audit/login.html')
    return inner


def login(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('pwd')
        obj = models.Audit.objects.get(username=user, password=password)
        if obj:
            request.session['is_login'] = True
            request.session['username'] = obj.username
            request.session['role'] = 'audit'
            return HttpResponse(json.dumps({'status': True}))
        else:
            return HttpResponse(json.dumps({'status': False}))
    return render(request, 'Audit/login.html')


@is_login
def project(request):
    if request.method == 'POST':
        data = {'status': True, 'projects':[]}
        n = int(request.POST.get('n'))
        projects = Projects.objects.filter(status=n)
        for project in projects:
            _project = project.__dict__
            del _project['_state']
            _project['time_limit'] = _project['time_limit'].strftime("%Y-%m-%d")
            data['projects'].append(_project)
        print(data)
        return HttpResponse(json.dumps(data))
    return render(request, 'Audit/audit.html')


@is_login
def project_profile(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        advice = request.POST.get('advice')
        batch = int(request.POST.get('batch'))
        status = int(request.POST.get('status'))
        if status != 3:
            status = batch + 1
        user_id = models.Audit.objects.get(username=request.session.get('username')).id
        pro = Projects.objects.filter(id=id)
        pro.update(status=status)
        models.Advice.objects.create(project_id=id,
                                     advice=advice,
                                     batch=batch,
                                     user_id=user_id)
        if status == 2:
            values = {'funder': pro[0].sender, 'brief': pro[0].goal, 'companyID': pro[0].id, 'award': pro[0].award}
            utils.new_company_add(values)
            utils.mine_company()
            path = os.path.join(BASE_DIR,'file_pag', pro[0].name)
            dic, key = utils.file_to_dict(path)
            value = {'funder': pro[0].sender, 'companyID': pro[0].id, 'funder_prove': {},'company_prove': dic}
            utils.new_prove_add(value)
            utils.mine_prove()
            # email = UserInfo.objects.get(name=pro[0].sender).email
            utilsb.send_mail(pro[0].sender, key, True, pro[0].name)
            utils.verify_chain()
            shutil.rmtree(path)
        return HttpResponse(json.dumps({'status': True}))
    pr_id = request.GET.get('pr')
    if pr_id:
        pro = Projects.objects.get(id=pr_id)
    else:
        pro = None
    return render(request, 'Audit/jiucai.html', {'project': pro})


@is_login
def download(request):
    #下载项目附件
    path = request.GET.get('path')
    file_name = path.split('\\')[1]
    response = StreamingHttpResponse(utils.file_iter(path, 512))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response
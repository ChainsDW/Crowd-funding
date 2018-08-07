from django import template
import time
from jiuchai import models
from django.utils.safestring import mark_safe
from jiuchai.utils import utils

register = template.Library()


@register.simple_tag()
def render_time(timer):
    sec = float(timer)
    timer = time.struct_time(time.localtime(sec))
    return time.strftime("%Y-%m-%d %H:%M:%S", timer)


@register.simple_tag()
def count_trans(transactions):
    return len(transactions)


@register.simple_tag()
def render_project_name(cid):
    if cid == 0:
        return '挖矿'
    project = models.Projects.objects.get(id=cid)
    return project.name


@register.simple_tag()
def render_a_tag(status, cid):
    if not bool(status):
        a = '<button type="button" class="btn btn-default"><a href="/transactions/' \
            'new?pr={}">支持该项目</a></button>'.format(cid)
    else:
        a = '<button type="button" class="btn btn-default" disabled="true">已完成筹资</button>'
    return mark_safe(a)


@register.simple_tag()
def each_project_trans(cid):
    """
    :param cid: 项目ID
    :return: TR
    """
    trs = []
    tr = '<tr>'
    chains = utils.full_chain()
    for block in chains['chain']:
        if int(cid) in block['companyID']:
            if 'transactions' in block.keys():
                for tran in block['transactions']:
                    if 'companyID' in tran.keys() and tran['companyID'] == int(cid):
                        tr += '<td>'+str(block['index']) + '</td><td>'+tran['sender'] + '</td><td>' + tran['recipient'] +\
                              '</td><td>' + str(tran['amount']) + '</td><td>' + str(tran['status']) + '</td><td>' + \
                              str(tran['stage']) + '</td><td>'+render_time(tran['timestamp']) + '</td></tr>'
                        trs.append(tr)
                        tr = '<tr>'
    final = ' '.join(trs)
    return mark_safe(final)


@register.simple_tag()
def render_project(cid):
    """
    :param cid: 项目ID
    :return: TR项目计划和回报
    """
    tr = '<tr>'
    chains = utils.full_chain()
    for block in chains['chain']:
        if 'introduction' in block.keys():
            if block['introduction'][0]['companyID'] == int(cid):
                tr += '<td>' + block['introduction'][0]['brief'] + '</td><td>' + block['introduction'][0]['award'] + '</td>'
    return mark_safe(tr)

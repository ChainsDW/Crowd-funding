from jiuchai.utils import utils
from jiuchai import models


def count_project_amount(project):
    """
    :param project:项目ID
    :return: 项目名称筹资总额
    """
    count = 0
    chains = utils.full_chain()
    for block in chains['chain']:
        if int(project) in block['companyID']:
            if 'transactions' in block.keys():
                for tran in block['transactions']:
                    if 'companyID' in tran.keys() and 'status' in tran.keys():
                        if tran['companyID'] == int(project) and tran['status'] == 'promise':
                            count += int(tran['amount'])
    return count


def count_somebody_amount(sender,cid):
    """
    :param sender: 投资人
    :param cid: 投资项目ID
    :return: 投资人在此项目上投资总额
    """
    chains = utils.full_chain()
    count = 0
    for block in chains['chain']:
        if int(cid) in block['companyID']:
            for tran in block['transactions']:
                if tran['sender'] == sender and tran['companyID'] == cid:
                    count += int(tran['amount'])
    return count


def count_somebody_mining_time(sender):
    chains = utils.full_chain()
    count = 0
    for block in chains['chain']:
            for tran in block['transactions']:
                if tran['sender'] == sender and tran['mining_time']:
                    count += int(tran['mining_time'])
    return count


def find_prove_dic(pro_id):
    """
    :param pro_id:
    :return: 资料字典 {'文件名'：'数据'}
    """
    chain = utils.full_chain()
    for block in chain['chain']:
        if int(pro_id) in block['companyID'] and 'company_prove' in block.keys():
            return block['company_prove'][0]['company_prove']  #没有考虑资料更新


def find_user_project(email, types):
    """
    :return: 返回用户所有交易的项目ID和对应的金额
            {'companyID':amount,...}
    """
    project_dict = {}
    chain = utils.full_chain()
    for block in chain['chain']:
        if 'transactions' in block.keys():
            for trans in block['transactions']:
                if trans['sender'] == email and trans['status'] == types:
                    if trans['companyID'] in project_dict.keys():
                        project_dict[trans['companyID']] += trans['amount']
                    else:
                        project_dict[trans['companyID']] = trans['amount']
    return project_dict

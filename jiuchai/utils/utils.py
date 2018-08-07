import os
from xuejieBT.settings import BASE_DIR
import pickle
from jiuchai.utils.blockchain import *
from jiuchai.utils import AES
import random
from jiuchai import models
import zipfile


# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

funder = "江南皮革厂"
time_goal = 100
money_goal = 20


def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # 给工作量证明的节点提供奖励.
    # mining_time作为统计每次挖矿次数的变量，原理与挖矿奖励的代币相同。
    blockchain.new_mining_time(
        sender="wotou",
        recipient=node_identifier,
        mining_time=1,
    )

    # Forge the new Block by adding it to the chain
    block = blockchain.new_block(proof, None)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'comoanyID':block['companyID'],
    }
    return response


def mine_prove():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # 给工作量证明的节点提供奖励.
    # 发送者为 "0" 表明是新挖出的币
    blockchain.new_mining_time(
        sender="wotou",
        recipient=node_identifier,
        mining_time=1,
    )

    # Forge the new Block by adding it to the chain
    block = blockchain.new_company_prove(proof, None)

    return True

def mine_proposal():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # 给工作量证明的节点提供奖励.
    # 发送者为 "0" 表明是新挖出的币
    blockchain.new_mining_time(
        sender="wotou",
        recipient=node_identifier,
        mining_time=1,
    )

    # Forge the new Block by adding it to the chain
    block = blockchain.new_block_proposal(proof, None)

    return True


def mine_company():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    # Forge the new Block by adding it to the chain
    block = blockchain.new_company_block(proof, None)
    response = {
        'message': "New introduction Forged",
        'index': block['index'],
        'introduction': block['introduction'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'comoanyID':block['companyID'],
    }
    return response


def new_transaction(values):
    # values = request.POST.get('data')
    print(values['sender'])
    # 检查POST数据
    required = ['sender', 'recipient', 'amount','companyID','status','stage']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'], values['companyID'],values['status'],values['stage'])

    response = {'message': 'Transaction will be added to Block ' + str(index)}
    return response


def new_company_add(values):
    # values = request.POST.get('data')
    #目前填入项目数据不会提供奖励，因为这个只能咱们来填，这个是预留的一个后门
    print(values['funder'])
    # 检查POST数据
    required = ['funder', 'brief', 'award','companyID']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_company(values['funder'], values['brief'], values['award'], values['companyID'])

    response = {'message': 'introduction will be added to Block ' + str(index)}
    return response


def new_prove_add(values):
    # values = request.POST.get('data')
    print(values['funder'])
    # 检查POST数据
    required = ['funder', 'companyID', 'funder_prove','company_prove']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_prove(values['funder_prove'], values['company_prove'], values['funder'],  values['companyID'])

    response = {'message': 'prove_information will be added to Block ' + str(index)}
    return response


def new_proposal_add(values):
    # values = request.POST.get('data')
    print(values['sender'])
    # 检查POST数据
    required = ['sender', 'proposal', 'vote_participant','oppose_participant','companyID','flag']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_proposal(values['funder_prove'], values['company_prove'], values['funder'],  values['companyID'])

    response = {'message': 'prove_information will be added to Block ' + str(index)}
    return response

def full_chain():
    #查看所有区块
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return response


def register_nodes(values):
    nodes = values.get('nodes')
    print(type(nodes))
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    #for node in nodes:
    blockchain.register_node(nodes)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return response


def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return response


def file_iter(path,chunck_size):
    #返回文件流
    with open(os.path.join(BASE_DIR, 'file_pag', path), 'rb') as f:
        while True:
            c = f.read(chunck_size)
            if c:
                yield c
            else:
                break


def verify_chain():
    chain = full_chain()
    file_adr = os.path.join(BASE_DIR, 'blockchain_copy', 'chain.pkl')
    file = open(file_adr, 'rb')
    data = file.read()
    if data:
        file_chain = pickle.loads(data)
        if file_chain['chain'] == chain['chain']:
            return True, file.close()
        elif len(file_chain['chain']) > len(chain['chain']):
            consensus()
        else:
            download_chain(file_adr)
    else:
        download_chain(file_adr)


def download_chain(file_adr):
    chain = full_chain()
    file = open(file_adr, 'wb')
    file.write(pickle.dumps(chain))
    file.close()


# def imange_to_binary(path):
#     """
#     :param path:文件路径
#     :return:
#     """
#     image = cv2.imread(path)
#     rows = image.shape[0]
#     cols = image.shape[1]
#     #把图像转换为二进制文件
#     #python写二进制文件，f = open('name','wb')
#     #只有wb才是写二进制文件
#     fileSave = open('patch.bin','wb')
#     for step in range(0,rows):
#         for step2 in range(0,cols):
#             fileSave.write(image[step,step2,2])
#     for step in range(0,rows):
#         for step2 in range(0,cols):
#             fileSave.write(image[step,step2,1])
#     for step in range(0,rows):
#         for step2 in range(0,cols):
#             fileSave.write(image[step,step2,0])
#     fileSave.close()

def file_to_dict(path):
    """
    :param path:文件夹路径
    :return: dict， key
    """
    key = random_key()
    dic = {}
    lis = os.listdir(path)
    file_name = None
    for i in range(0, len(lis)):
        if os.path.splitext(lis[i])[1] == '.zip':
            file_zip = zipfile.ZipFile(os.path.join(path,lis[i]), 'r')
            for file in file_zip.namelist():
                file_zip.extract(file, path)
            file_zip.close()
            file_name = os.path.splitext(lis[i])[0]
            os.remove(os.path.join(path, lis[i]))
    path = os.path.join(path, file_name)
    lis = os.listdir(path)
    for i in range(0, len(lis)):
        file_adr = os.path.join(path, lis[i])
        with open(file_adr, 'rb') as f:
            data = f.read()
        code = AES.PrpCrypt(key)
        data = code.encrypt(data)
        file = lis[i]
        dic[file] = data
    return dic, key


def dic_to_file(key, dic, pro_name):
    """
    :param dic:字典
    :param key:密钥
    :param pro_name:文件名
    :return:
    通过dic创建文件
    """
    path = os.path.join(BASE_DIR, 'file_pag', pro_name)
    zip_name = os.path.splitext(models.Projects.objects.get(name=pro_name).file_adr.split('\\')[1])[0]
    try:
        os.makedirs(path)
    except Exception:
        pass
    print(dic)
    for i, v in dic.items():
        code = AES.PrpCrypt(key)
        file = i
        data = code.decrypt(v)
        file_adr = os.path.join(path, file)
        with open(file_adr, 'wb') as f:
            f.write(data)
    f = zipfile.ZipFile(os.path.join(path, zip_name+'.zip'), 'w', zipfile.ZIP_DEFLATED)
    print(path)
    if os.path.isdir(path):
        for d in os.listdir(path):
            if os.path.splitext(d)[1] != '.zip':
                f.write(os.path.join(path, d), d)
    f.close()
    for i in os.listdir(path):
        if os.path.splitext(i)[1] != '.zip':
            os.remove(os.path.join(path, i))



def random_key():
    """
    :return:随机16位密钥
    """
    code = ''
    for i in range(16):
        current = random.randrange(0,16)
        if current != i and current % 2 == 0:
            temp = random.randint(0, 9)
        else:
            temp = chr(random.randint(65, 90))
        code += str(temp)
    return code



if __name__ == '__main__':
    a = bytes('asa', 'utf8')
    print(a)
# coding:utf-8
import hashlib
import pickle
import json
from time import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
from uuid import uuid4
import os
from xuejieBT.settings import BASE_DIR
import requests
from jiuchai.utils.auto_get_data import count_somebody_mining_time
import threading


class Blockchain:
    def __init__(self):
        self.current_transactions = [] #交易信息
        self.current_introduction=[] #
        self.chain = []
        self.nodes = set()
        self.companyID = []
        self.current_prove =[]
        self.funder_prove = []
        self.company_prove = []
        self.mining_time =[]
        self.current_proposal = []

        # 创建创世块
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address: str) -> None:
        """
        Add a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain: List[Dict[str, Any]]) -> bool:
        """
        Determine if a given blockchain is valid

        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            #print(f'{last_block}')
            print(last_block)
            #print(f'{block}')
            print(block)
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self) -> bool:
        """
        共识算法解决冲突
        使用网络中最长的链.

        :return:  如果链被取代返回 True, 否则为False

        """
        file_adr = os.path.join(BASE_DIR, 'blockchain_copy', 'chain.pkl')
        file = open(file_adr, 'rb')
        chain = file.read()
        if chain:
            self.chain = pickle.loads(chain)['chain']
            print(self.chain)
        neighbours = self.nodes
        new_chain = None
        new_nodes = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)
        max_nodes =len(self.nodes)
        max_weights = 0

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            #response = requests.get(f'http://{node}/chain')
            response = requests.get('http://'+node+'/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                last_chain = chain[-1]
                last_proof = last_chain['proof']#获取最后一个块的工作量证明
                last_recipient = last_chain['recipient']
                #假设已经得到了mining_time的全部余额
                mining_times = count_somebody_mining_time(last_recipient)
                #求出权重值
                last_weight = 2*(mining_times*last_proof)/(mining_times+last_proof)
                nodes = self.nodes
                if last_weight>max_weights:
                    max_weights = last_weight
                    lengths = response.json()['length']
                    chains = response.json()['chain']


                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
                elif length == max_length and self.valid_chain(chain):
                    max_length = lengths
                    new_chain = chains
                if len(nodes)>max_nodes and self.valid_chain(chain):
                    new_nodes = nodes

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain

        if new_nodes:
            self.nodes = new_nodes
            return True

        return False

    def new_block(self, proof: int, previous_hash: Optional[str]) -> Dict[str, Any]:
        """
        生成新块

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'companyID':self.companyID,
        }

        # Reset the current list of transactions
        self.current_transactions = []
        self.companyID = []
        self.chain.append(block)
        return block


    def new_transaction(self, sender: str, recipient: str, amount: int, companyID: int, status: str, stage: str) -> int:
        """
        生成新交易信息，信息将加入到下一个待挖的区块中

        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': time(),
            'companyID': companyID,
            'status': status,
            'stage': stage,
        })
        if companyID not in self.companyID:
            self.companyID.append(companyID)
        return self.last_block['index'] + 1

    @property
    def last_block(self) -> Dict[str, Any]:
        return self.chain[-1]

    @staticmethod
    def hash(block: Dict[str, Any]) -> str:
        """
        生成块的 SHA-256 hash值

        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = pickle.dumps(block)
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof: int) -> int:
        """
        简单的工作量证明:
         - 查找一个 p' 使得 hash(pp') 以4个0开头
         - p 是上一个块的证明,  p' 是当前的证明
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        """
        验证证明: 是否hash(last_proof, proof)以4个0开头

        :param last_proof: Previous Proof
        :param proof: Current Proof
        :return: True if correct, False if not.
        """

        #guess = f'{last_proof}{proof}'.encode()
        guess = str(last_proof).encode() + str(proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:2] == "00"

#introduction块
    def new_company(self, funder: str, brief: str,award: str ,companyID: int,) -> int:
        self.current_introduction.append({
            'funder': funder,
            'brief': brief,
            'award': award,
            'timestamp': time(),
            'companyID':companyID,
        })
        return self.last_block['index'] + 1

    def new_company_block(self, proof: int, previous_hash: Optional[str]) -> Dict[str, Any]:
        """
        生成新块

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """
        print(self.chain[-1])
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'introduction': self.current_introduction,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'companyID': self.companyID,
        }

        # Reset the current list of transactions
        self.current_introduction = []
        self.companyID = []
        self.chain.append(block)
        return block

#认证信息块
    def new_prove(self, funder_prove: str, company_prove: str,funder: str ,companyID: int,) -> int:
        self.current_prove.append({
            'funder': funder,
            'companyID': companyID,
            'funder_prove': funder_prove,
            'company_prove': company_prove,
        })
        self.companyID.append(companyID)
        return self.last_block['index'] + 1

    def new_company_prove(self, proof: int, previous_hash: Optional[str]) -> Dict[str, Any]:
        """
        生成新块

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'company_prove': self.current_prove,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'companyID': self.companyID,
        }

        # Reset the current list of transactions
        self.current_prove = []
        self.companyID = []
        self.chain.append(block)
        return block


    def new_mining_time(self, sender: str, recipient: str, mining_time: int) -> int:
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'mining_time': mining_time,
            'timestamp': time(),
        })
        return self.last_block['index'] + 1



    def new_block_proposal(self, proof: int, previous_hash: Optional[str]) -> Dict[str, Any]:

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'proposal': self.current_proposal,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'companyID':self.companyID,
        }

        # Reset the current list of transactions
        self.current_proposal= []
        self.chain.append(block)
        return block


    def new_proposal(self, sender: str, proposal: str, vote_participant: str, oppose_participant: int,companyID: int, flag: str) -> int:
        #传入的flag是用来表示提议是否通过的状态
        self.current_proposal.append({
            'sender': sender,
            'proposal': proposal,
            'vote_participant': vote_participant,
            'oppose_participant': oppose_participant,
            'companyID': companyID,
            'flag': flag,
        })
        if companyID not in self.companyID:
            self.companyID.append(companyID)
        return self.last_block['index'] + 1




    def paxos(self,num):
        #传入的节点数量需为奇数，默认为3
        for i in range(num):
            threads = []
            i = threading.Thread(target=self.resolve_conflicts)
            threads.append(i)
            for t in threads:
                t.setDaemon(False)
                t.start()
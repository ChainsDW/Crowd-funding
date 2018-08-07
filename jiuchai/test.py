import time
import hashlib
import pickle

# a = '1531826734.077628'
# print(float(a))
# print(time.ctime(float(a)))
# c = '0'
# a = '123124124'
# with open(r'F:\智诚\Django重置版本（1.9）(1).zip', 'rb') as f:
#     b = f.read()
# with open(r'F:\Django重置版本（1.9）(1).zip', 'wb') as f:
#     f.write(b)

# data = hashlib.sha256(b).hexdigest()
# print('1',data)
import image
# funder_prove = {}
# with open(r'F:\20130127_205501.jpg', 'rb') as f:
#     c = f.read()
# funder_prove['20130127_204646.jpg'] = c
# print(funder_prove)

# x = '12das'
# print(x.encode())

import json
# ss = {'das': [{'123':123}]}
# with open(r'F:\智诚\Django重置版本（1.9）\blockchain_copy\chain.json', 'r') as f:
#     chain = json.loads(f.read())
#     print(chain['chain'])
# # with open(r'F:\智诚\Django重置版本（1.9）\blockchain_copy\chain.json', 'w') as f:
# #     f.write(json.dumps(ss))
#
# print(type(chain['chain'][1]['companyID'][0]))

# dic = {'123': 12}
# for i,v in dic.items():
#     print(i,v)
# class MyEncoder(json.JSONEncoder):
#
#     def default(self, obj):
#         if isinstance(obj, bytes):
#             return str(obj, encoding='utf-8')
#         return json.JSONEncoder.default(self, obj)
#
#
# with open(r'F:\AA\20130127_205501.jpg', 'rb') as f:
#     a = f.read()
# a_string = '{}'.format(a).split('\'')[1]
# s = {'asd':[a]}
# cc = pickle.dumps(s)
# with open(r'F:\AA\1.pkl', 'wb') as f:
#     f.write(cc)
# with open(r'F:\AA\1.pkl', 'rb') as f:
#     ss = f.read()
# op = pickle.loads(ss)
# print(type(op['asd']))
#
# with open(r'F:\AA\1.jpg', 'wb') as f:
#     f.write(op)

# with open(r'F:\智诚\Django重置版本（1.9）\blockchain_copy\chain.pkl', 'rb') as f:
#     ss = f.read()
#
# print(pickle.loads(ss)['chain'])
import zipfile
import os
# f = zipfile.ZipFile(r'F:\AA\asd\aa.zip', 'w', zipfile.ZIP_DEFLATED)
# if os.path.isdir(r'F:\AA\asd'):
#      for d in os.listdir(r'F:\AA\asd'):
#          if os.path.splitext(d)[1] != '.zip':
#             f.write(os.path.join(r'F:\AA\asd',d),d)
#          # close() 是必须调用的！
# f.close()

# askdo = {}
#
# askdo['1'] = int()
# askdo['1'] += 2
# askdo['1'] = int()
# print(askdo['1'])
# print(time.time())
import datetime
# a = datetime.datetime(2018,2,2)
c = datetime.date.today()
# sc =(c-a).days
# print(sc)
a = datetime.datetime.strftime(c, "%Y-%m-%d")
print(a, type(a))
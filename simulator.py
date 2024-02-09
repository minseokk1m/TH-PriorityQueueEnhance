from typing import (
  Callable,
  NewType,
  Union,
)
from web3 import Web3, module
from web3.method import (
  Method,
  default_root_munger,
)
from web3.types import (
  BlockNumber,
  RPCEndpoint,
)

import pymysql.cursors
import time
import threading
import json
import rlp
import binascii

db_host = 'localhost'
db_user = 'ethereum'
db_pass = '' #fill in the MariaDB/MySQL password.
db_name = 'ethereum'

# geth_ipc = './bin/data/geth.ipc' #fill in the IPC path.
# geth_ipc = '~/TrieHashimoto/vscnode2node/blkchain1/geth.ipc' #fill in the IPC path.
geth_ipc = '/data/THEnhanceSyncData/tempblkchain1/geth.ipc'

num_block = 1 # number of blocks to make at once
epoch = 3 # inactivate epoch
restore_offset = 0
password = '1234' #fill in the geth coinbase password.

EthToWei = 1000000000000000000

MODE_ETHANOS = 0
MODE_ETHANE = 1
execution_mode = MODE_ETHANE

RESTORE_ALL = 0
RESTORE_RECENT = 1
RESTORE_OLDEST = 2
RESTORE_OPTIMIZED = 3 # If the amount is given as an input, then automatically restore the least accounts whose sum is bigger than the amount
restore_amount = '50' # requesting amount to be restored (only RESTORE_OPTIMIZED mode)
restore_mode = RESTORE_ALL

# restorefile = 'restore_test.json'

NUM_NORMAL_TX = 200
OFFSET_ADDR = 1

conn_geth = lambda path: Web3(Web3.IPCProvider(path))
# conn_mariadb = lambda host, user, password, database: pymysql.connect(host=host, user=user, password=password, database=database, cursorclass=pymysql.cursors.DictCursor)

class Debug(module.Module):
  def __init__(self, web3):
    module.Module.__init__(self, web3)
  
  setHead: Method[Callable[[BlockNumber], bool]] = Method(
    RPCEndpoint("debug_setHead"),
    mungers=[default_root_munger],
  )

Nonce = NewType("Nonce", int)
Wei = NewType('Wei', int)

class Custom(module.Module):
  def __init__(self, web3):
    module.Module.__init__(self, web3)

class Worker(threading.Thread):
  def __init__(self, web3, tx):
    threading.Thread.__init__(self)
    self.web3 = web3
    self.tx = tx
  
  def run(self):
    self.web3.eth.send_transaction(self.tx)
  

def run(num):
  web3 = conn_geth(geth_ipc)
  # conn = conn_mariadb(db_host, db_user, db_pass, db_name)

  web3.attach_modules({
    'debug': Debug,
    'custom': Custom,
  })

  #web3.debug.setHead('0x0')

  # print("coinbase 전까지는 잘옴 ")
  coinbase = web3.eth.coinbase
  # print("coinbase: ", coinbase)
  web3.geth.personal.unlock_account(coinbase, password, 0)

  # stop mining
  web3.geth.miner.stop()

  offset_block = web3.eth.get_block_number() + 1 # _from # - 1
  realblock = 0

  # print('Account {} unlocked'.format(coinbase))
  # print('Run from {} to {}'.format(offset_block, offset_block+num-1))

  for i in range(num):
    currentBlock = web3.eth.get_block_number()
    print("currentBlock: ", currentBlock)
    workers = []

    """ NORMAL TX """
    for j in range(NUM_NORMAL_TX): # for each tx in one block
      # print("currentBlock+j",currentBlock*NUM_NORMAL_TX+j)
      to = intToAddr(int(currentBlock*NUM_NORMAL_TX+j))
      amount = int(currentBlock*NUM_NORMAL_TX+j)
      tx = {
        'from': coinbase,
        'to': to,
        'value': amount,
        'gas': '21000',
        # 'nonce': hex(int(i*NUM_NORMAL_TX+j)),
        'data': '',
      }

      # print("NORMAL TX")
      # print(tx)

      worker = Worker(web3, tx)
      worker.start()
      workers.append(worker)
    
    """ MINING """
    for j in workers:
      j.join()

    # print('Block #{}: processed all txs'.format(i))
    
    web3.geth.miner.start(1)
    while (web3.eth.get_block_number() == currentBlock):
      # time.sleep(0.001)
      pass # just wait for mining
    web3.geth.miner.stop()

    realblock = web3.eth.get_block_number()
    # print('Mined block #{}'.format(realblock))

    # print('='*60)

def intToAddr(num):
    intToHex = f'{num:0>40x}'
    return Web3.toChecksumAddress("0x" + intToHex)

for j in range(100):
  run(num_block)
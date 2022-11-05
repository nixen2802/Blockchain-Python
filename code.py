import random
from Crypto.PublicKey import RSA
import string
import hashlib
import time
import rsa
base_address=''.join(random.choices(string.ascii_uppercase + string.digits, k = 16))    
base_address = "0x"+str(base_address)
previous_address=''.join(random.choices(string.ascii_uppercase + string.digits, k = 16))    
previous_address = "0x"+str(base_address)
class User:
    def __init__(self):
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 16))    
        self.user_address = "0x"+str(ran)
        pri_key = RSA.generate(1024)
        self.pub_key = pri_key.publickey().exportKey().decode("utf-8")
        self.pri_key=pri_key


class UTXO:
    def __init__(self, user_address, unspent):
        self.user_address=user_address
        self.unspent=unspent

class DB_UTXO:
  def __init__(self, utxos):
    self.utxo_transactions=[]
    for i in utxos:
      self.utxo_transactions.append(i)

class Transactions:
    def __init__(self, from_address, to_address, amount, digital_signature):
        self.from_address=from_address
        self.to_address=to_address
        self.amount=amount
        self.digital_signature=digital_signature

class Block:
  def __init__(self, block_number, previous_hash, nonce, timestamp, block_hash, merkle, transactions):
    self.block_number=block_number
    self.previous_hash=previous_hash
    self.nonce=nonce
    self.timestamp=timestamp
    self.block_hash=block_hash
    self.merkle=merkle
    self.transactions=transactions

users=[]
utxos=[]
temp_utxos=[]
for i in range(0, 4):
  amount=random.uniform(0,100)
  users.append(User())
  utxos.append(UTXO(users[i].user_address, amount))
  if(i==3):
    temp_utxos.append([users[i].user_address, 0])
    break
  temp_utxos.append([users[i].user_address, amount])  

utxo_database=DB_UTXO(temp_utxos)

transactions=[]
for i in range(0, 3):
  temp=random.randint(0,2)
  while(True):
    temp2=random.randint(0,2)
    if(temp!=temp2):
      amount=random.uniform(0,50)
      temp_str_val=str(users[temp].user_address)+str(users[temp2].user_address)+str(amount)
      hash = hashlib.sha256(temp_str_val.encode())
      transactionHash = hash.hexdigest()
      encTransaction = rsa.encrypt(transactionHash.encode(), users[temp].pri_key)
      transactions.append(Transactions(users[temp].user_address, users[temp2].user_address, amount, encTransaction))
      break


def validate(transaction, pri, pub):
  val=0
  print("Digital signature verification started.......")
  print("-"*100)
  decMessage = rsa.decrypt(transaction.digital_signature, pub).decode()
  print("Digital signature verified.......")
  print("-"*100)
  print("Validation process started.......")
  print("-"*100)
  for i in utxo_database.utxo_transactions:
    if i[0]==transaction.from_address:
      val=val+i[1]
  if val > transaction.amount+ transaction.amount*0.001:
        print("Valid transaction (Transaction added to the valid transactions pool)!")
        print("-"*100)
        return True
  print("Invalid transaction (Insufficient balance)!")
  print("-"*50)
  return False

def mining(transaction, pri, pub):
  print("Digital signature verification started.......")
  print("-"*100)
  decMessage = rsa.decrypt(transaction.digital_signature, pub).decode()
  print("Digital signature verified.......")
  print("-"*100)
  data=str(transaction.from_address)+str(transaction.to_address)+str(transaction.amount)+str(transaction.amount*0.001)
  diff="0"
  nonce=0
  res=""
  print("Mining process started.......")
  print("-"*100)
  while(res[0:1]!=diff):
    str_nonce=str(nonce)
    nonce=nonce+1
    res=hashlib.sha256((data+str_nonce).encode())
    res=str(res.hexdigest())
  return nonce

def utxo_updation(transaction):
  i=0
  while(True):
    if(utxo_database.utxo_transactions[i][0]==transaction.from_address):
      utxo_database.utxo_transactions.pop(i)
    else:
      i=i+1
    if(i==len(utxo_database.utxo_transactions)):
      break

def bal_calc(address):
  val=0
  for i in utxo_database.utxo_transactions:
    if i[0]==address:
      val=val+i[1]
  return val

def address_calculation(transaction):
  data=str(transaction.from_address)+str(transaction.to_address)+str(transaction.amount)+str(transaction.amount*0.001)
  res=""
  res=hashlib.sha256((data).encode())
  res=str(res.hexdigest())
  return res

def block_hash_calculator(index, previous_address, min, timevalue, merkle):
  data=str(index)+str(previous_address)+str(min)+str(timevalue)+str(merkle)
  res=""
  res=hashlib.sha256((data).encode())
  res=str(res.hexdigest())
  return res  

def user_finder(address):
  for i in range(0, len(users)):
    if users[i].user_address==address:
      return users[i].pri_key, users[i].pub_key


blockchain=[]
ind=1

print("-"*100)
print("-"*100)
print("Private Blockchain Implementation")
print("-"*100)
print("Difficulty level: 1")
print("Transaction fees: 0.1% of transaction amount")
print("Mining reward: 6.25")
print("Digital signature algorithm: RSA")
print("Token data model: UTXO")
print("-"*100)
print("-"*100)
print("UTXO")
print("-"*100)
print("Address\t\t\tAmount")
print("-"*100)
for i in utxo_database.utxo_transactions:
  if(i[0]==users[3].user_address):
    print(i[0], " -> ", i[1], "(Miner)")
  else:
    print(i[0], " -> ", i[1])
print("-"*100)
print("User balanaces")
print("-"*100)
for j in range(0, 4):
  if(j!=3):
    print(users[j].user_address, "->", bal_calc(users[j].user_address))
  else:
    print(users[j].user_address, "->", bal_calc(users[j].user_address), "(Miner)")
print("-"*100)
print("Transactions (neither validated nor verified)")
print("-"*100)
for j in range(0, 3):
  print(transactions[j].from_address, " -> ", transactions[j].to_address, " Amount: ", transactions[j].amount)
print("-"*150)

for i in range(0, 3):
  print("Transaction in process: ",i," : ", transactions[i].from_address, "->", transactions[i].to_address, " Amount: ", transactions[i].amount, ", TXN Fees", transactions[i].amount*0.001)
  print("-"*150)
  print("Validator node: ")
  print("-"*100)
  pri, pub=user_finder(transactions[i].from_address)
  val=validate(transactions[i], pri, pub)
  if(val==True):
    pri, pub=user_finder(transactions[i].from_address)
    print("Miner node: ")
    print("-"*100)
    print("Transaction ",i, "taken from pool of valid transactions!!!")
    print("-"*100)
    min=mining(transactions[i], pri, pub)
    merkle=address_calculation(transactions[i])
    print("Mining process finished: Nonce = ", min)
    print("-"*100)
    utxo_database.utxo_transactions.append([transactions[i].to_address, transactions[i].amount])
    bal=bal_calc(transactions[i].from_address)
    utxo_updation(transactions[i])
    utxo_database.utxo_transactions.append([transactions[i].from_address, bal-transactions[i].amount-transactions[i].amount*0.001])
    print("Block creation process started.......")
    print("-"*100)
    time_value=time.time()
    block_hash=block_hash_calculator(ind, previous_address, min, time_value, merkle)
    block=Block(ind, previous_address, min, time_value, block_hash, merkle, [transactions[i], [base_address, transactions[i].from_address, bal-transactions[i].amount-transactions[i].amount*0.001]])
    ind=ind+1
    previous_address=block_hash
    blockchain.append(block)
    utxo_database.utxo_transactions.append([users[-1].user_address, 6.25+transactions[i].amount*0.001])
    print("Block created.......")
    print("-"*100)
    print("Block broadcasted to all the other nodes.......")
    print("-"*100)
    print("All the nodes validates the block (consensus).......")
    print("-"*100)
    print("Block added to the blockchain.......")
    print("-"*100)
    print("-"*100)
    print("Transaction fees and block reward paid to the miner")
    print("-"*100)
    print("Miner balance: ", bal_calc(users[-1].user_address))
    print("-"*100)
    print("User balances")
    print("-"*100)
    for j in range(0,3):
      print(users[j].user_address, "->", bal_calc(users[j].user_address))
    print(users[3].user_address, "->", bal_calc(users[3].user_address), "(Miner)")
    print("-"*100)
  print("-"*100)
  print("UTXO")
  print("-"*100)
  print("Address\t\t\tAmount")
  print("-"*100)
  for i in utxo_database.utxo_transactions:
    if(i[0]==users[3].user_address):
      print(i[0], " -> ", i[1], "(Miner)")
    else:
      print(i[0], " -> ", i[1])
  print("-"*100)
  print("Blockchain")
  print("-"*100)
  for i in blockchain:
    print("Block header")
    print("-"*100)
    print("Block number: ", i.block_number)
    print("Previous address: ", i.previous_hash)
    print("Nonce: ", i.nonce)
    print("Timestamp: ", i.timestamp)
    print("Merkle: ", i.merkle)
    print("-"*100)
    print("Block data")
    print("-"*100)
    print("Block hash: ", i.block_hash)
    print("Transactions: ")
    print(i.transactions[0].from_address, " -> ", i.transactions[0].to_address, " Amount: ", i.transactions[0].amount)
    print(i.transactions[1][0], " -> ", i.transactions[1][1], " Amount: ", i.transactions[1][2])
    print("-"*100)
    print("-"*100)
  print("-"*150)
import random
from Crypto.PublicKey import RSA
import string
import hashlib
import time
import rsa
base_address=''.join(random.choices(string.ascii_uppercase + string.digits, k = 16))    
base_address = "0x"+str(base_address)
previous_address=''.join(random.choices(string.ascii_uppercase + string.digits, k = 16))    
previous_address = "0x"+str(base_address)
class User:
    def __init__(self):
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 16))    
        self.user_address = "0x"+str(ran)
        pri_key = RSA.generate(1024)
        self.pub_key = pri_key.publickey().exportKey().decode("utf-8")
        self.pri_key=pri_key


class UTXO:
    def __init__(self, user_address, unspent):
        self.user_address=user_address
        self.unspent=unspent

class DB_UTXO:
  def __init__(self, utxos):
    self.utxo_transactions=[]
    for i in utxos:
      self.utxo_transactions.append(i)

class Transactions:
    def __init__(self, from_address, to_address, amount, digital_signature):
        self.from_address=from_address
        self.to_address=to_address
        self.amount=amount
        self.digital_signature=digital_signature

class Block:
  def __init__(self, block_number, previous_hash, nonce, timestamp, block_hash, merkle, transactions):
    self.block_number=block_number
    self.previous_hash=previous_hash
    self.nonce=nonce
    self.timestamp=timestamp
    self.block_hash=block_hash
    self.merkle=merkle
    self.transactions=transactions

users=[]
utxos=[]
temp_utxos=[]
for i in range(0, 4):
  amount=random.uniform(0,100)
  users.append(User())
  utxos.append(UTXO(users[i].user_address, amount))
  if(i==3):
    temp_utxos.append([users[i].user_address, 0])
    break
  temp_utxos.append([users[i].user_address, amount])  

utxo_database=DB_UTXO(temp_utxos)

transactions=[]
for i in range(0, 3):
  temp=random.randint(0,2)
  while(True):
    temp2=random.randint(0,2)
    if(temp!=temp2):
      amount=random.uniform(0,50)
      temp_str_val=str(users[temp].user_address)+str(users[temp2].user_address)+str(amount)
      hash = hashlib.sha256(temp_str_val.encode())
      transactionHash = hash.hexdigest()
      encTransaction = rsa.encrypt(transactionHash.encode(), users[temp].pri_key)
      transactions.append(Transactions(users[temp].user_address, users[temp2].user_address, amount, encTransaction))
      break


def validate(transaction, pri, pub):
  val=0
  print("Digital signature verification started.......")
  print("-"*100)
  decMessage = rsa.decrypt(transaction.digital_signature, pub).decode()
  print("Digital signature verified.......")
  print("-"*100)
  print("Validation process started.......")
  print("-"*100)
  for i in utxo_database.utxo_transactions:
    if i[0]==transaction.from_address:
      val=val+i[1]
  if val > transaction.amount+ transaction.amount*0.001:
        print("Valid transaction (Transaction added to the valid transactions pool)!")
        print("-"*100)
        return True
  print("Invalid transaction (Insufficient balance)!")
  print("-"*50)
  return False

def mining(transaction, pri, pub):
  print("Digital signature verification started.......")
  print("-"*100)
  decMessage = rsa.decrypt(transaction.digital_signature, pub).decode()
  print("Digital signature verified.......")
  print("-"*100)
  data=str(transaction.from_address)+str(transaction.to_address)+str(transaction.amount)+str(transaction.amount*0.001)
  diff="0"
  nonce=0
  res=""
  print("Mining process started.......")
  print("-"*100)
  while(res[0:1]!=diff):
    str_nonce=str(nonce)
    nonce=nonce+1
    res=hashlib.sha256((data+str_nonce).encode())
    res=str(res.hexdigest())
  return nonce

def utxo_updation(transaction):
  i=0
  while(True):
    if(utxo_database.utxo_transactions[i][0]==transaction.from_address):
      utxo_database.utxo_transactions.pop(i)
    else:
      i=i+1
    if(i==len(utxo_database.utxo_transactions)):
      break

def bal_calc(address):
  val=0
  for i in utxo_database.utxo_transactions:
    if i[0]==address:
      val=val+i[1]
  return val

def address_calculation(transaction):
  data=str(transaction.from_address)+str(transaction.to_address)+str(transaction.amount)+str(transaction.amount*0.001)
  res=""
  res=hashlib.sha256((data).encode())
  res=str(res.hexdigest())
  return res

def block_hash_calculator(index, previous_address, min, timevalue, merkle):
  data=str(index)+str(previous_address)+str(min)+str(timevalue)+str(merkle)
  res=""
  res=hashlib.sha256((data).encode())
  res=str(res.hexdigest())
  return res  

def user_finder(address):
  for i in range(0, len(users)):
    if users[i].user_address==address:
      return users[i].pri_key, users[i].pub_key


blockchain=[]
ind=1

print("-"*100)
print("-"*100)
print("Private Blockchain Implementation")
print("-"*100)
print("Difficulty level: 1")
print("Transaction fees: 0.1% of transaction amount")
print("Mining reward: 6.25")
print("Digital signature algorithm: RSA")
print("Token data model: UTXO")
print("-"*100)
print("-"*100)
print("UTXO")
print("-"*100)
print("Address\t\t\tAmount")
print("-"*100)
for i in utxo_database.utxo_transactions:
  if(i[0]==users[3].user_address):
    print(i[0], " -> ", i[1], "(Miner)")
  else:
    print(i[0], " -> ", i[1])
print("-"*100)
print("User balanaces")
print("-"*100)
for j in range(0, 4):
  if(j!=3):
    print(users[j].user_address, "->", bal_calc(users[j].user_address))
  else:
    print(users[j].user_address, "->", bal_calc(users[j].user_address), "(Miner)")
print("-"*100)
print("Transactions (neither validated nor verified)")
print("-"*100)
for j in range(0, 3):
  print(transactions[j].from_address, " -> ", transactions[j].to_address, " Amount: ", transactions[j].amount)
print("-"*150)

for i in range(0, 3):
  print("Transaction in process: ",i," : ", transactions[i].from_address, "->", transactions[i].to_address, " Amount: ", transactions[i].amount, ", TXN Fees", transactions[i].amount*0.001)
  print("-"*150)
  print("Validator node: ")
  print("-"*100)
  pri, pub=user_finder(transactions[i].from_address)
  val=validate(transactions[i], pri, pub)
  if(val==True):
    pri, pub=user_finder(transactions[i].from_address)
    print("Miner node: ")
    print("-"*100)
    print("Transaction ",i, "taken from pool of valid transactions!!!")
    print("-"*100)
    min=mining(transactions[i], pri, pub)
    merkle=address_calculation(transactions[i])
    print("Mining process finished: Nonce = ", min)
    print("-"*100)
    utxo_database.utxo_transactions.append([transactions[i].to_address, transactions[i].amount])
    bal=bal_calc(transactions[i].from_address)
    utxo_updation(transactions[i])
    utxo_database.utxo_transactions.append([transactions[i].from_address, bal-transactions[i].amount-transactions[i].amount*0.001])
    print("Block creation process started.......")
    print("-"*100)
    time_value=time.time()
    block_hash=block_hash_calculator(ind, previous_address, min, time_value, merkle)
    block=Block(ind, previous_address, min, time_value, block_hash, merkle, [transactions[i], [base_address, transactions[i].from_address, bal-transactions[i].amount-transactions[i].amount*0.001]])
    ind=ind+1
    previous_address=block_hash
    blockchain.append(block)
    utxo_database.utxo_transactions.append([users[-1].user_address, 6.25+transactions[i].amount*0.001])
    print("Block created.......")
    print("-"*100)
    print("Block broadcasted to all the other nodes.......")
    print("-"*100)
    print("All the nodes validates the block (consensus).......")
    print("-"*100)
    print("Block added to the blockchain.......")
    print("-"*100)
    print("-"*100)
    print("Transaction fees and block reward paid to the miner")
    print("-"*100)
    print("Miner balance: ", bal_calc(users[-1].user_address))
    print("-"*100)
    print("User balances")
    print("-"*100)
    for j in range(0,3):
      print(users[j].user_address, "->", bal_calc(users[j].user_address))
    print(users[3].user_address, "->", bal_calc(users[3].user_address), "(Miner)")
    print("-"*100)
  print("-"*100)
  print("UTXO")
  print("-"*100)
  print("Address\t\t\tAmount")
  print("-"*100)
  for i in utxo_database.utxo_transactions:
    if(i[0]==users[3].user_address):
      print(i[0], " -> ", i[1], "(Miner)")
    else:
      print(i[0], " -> ", i[1])
  print("-"*100)
  print("Blockchain")
  print("-"*100)
  for i in blockchain:
    print("Block header")
    print("-"*100)
    print("Block number: ", i.block_number)
    print("Previous address: ", i.previous_hash)
    print("Nonce: ", i.nonce)
    print("Timestamp: ", i.timestamp)
    print("Merkle: ", i.merkle)
    print("-"*100)
    print("Block data")
    print("-"*100)
    print("Block hash: ", i.block_hash)
    print("Transactions: ")
    print(i.transactions[0].from_address, " -> ", i.transactions[0].to_address, " Amount: ", i.transactions[0].amount)
    print(i.transactions[1][0], " -> ", i.transactions[1][1], " Amount: ", i.transactions[1][2])
    print("-"*100)
    print("-"*100)
  print("-"*150)

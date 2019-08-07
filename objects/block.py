
from util.string import String
from objects.transaction import LoadTransactions

import time

merkle_root = ""

class Block:
    def __init__(self, data, previous_hash):
        self.data = data
        self.previous_hash = previous_hash
        self.time_stamp = time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()
        self.transactions = []

    def calculate_hash(self):
        calculated_hash = String.apply_sha256(self.previous_hash +
                                              str(self.time_stamp) +
                                              str(self.nonce) +
                                              merkle_root)
        return calculated_hash

    def mine_block(self, difficulty):
        target = String.get_dificulty_string(difficulty)
        merkle_root = String.get_merkle_root(self.transactions)
        while(self.hash[:difficulty] != target):
            self.nonce += 1
            self.hash = self.calculate_hash()

        print("Block Mined!!! : " + self.hash) 

    def add_transaction(self, transaction, main_utxo):
        if(transaction == None):
            return False        

        if(self.previous_hash != "0"):
            if(transaction.process_transaction(main_utxo) != True):
                print("Transaction failed to process. Discarded.")
                return False

        self.transactions.append(transaction)
        print("Transaction Successfully added to Block")
        return True                        

#This is used to load blocks recorded at the blockchain.db
class LoadBlock(Block):
    def __init__(self , data , previous_hash , time_stamp , nonce , hash_value , transactions):
        self.data = data
        self.previous_hash = previous_hash
        self.time_stamp = time_stamp
        self.nonce = nonce
        self.hash = hash_value
        self.transactions = []

                                

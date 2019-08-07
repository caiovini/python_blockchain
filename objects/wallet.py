
from ellipticcurve.privateKey import PrivateKey
from objects.transaction import TransactionInput
from objects.transaction import Transaction
from constants import constants as const

class Wallet():
    def __init__(self):
        self.privateKey = PrivateKey()
        self.publicKey = self.privateKey.publicKey()
        self.utxo = {}

    def get_balance(self , main_utxo):
        total = 0
        for key, value in main_utxo.items():  
            utxo = value
            if(utxo.is_mine(self.publicKey)):
                self.utxo[utxo.id] = utxo
                total += utxo.value

        return total

    def send_funds(self, reciepient, value_sent , main_utxo):
        if(self.get_balance(main_utxo) < value_sent):
            print("#Not Enough funds to send transaction. Transaction Discarded.")
            return None

        total = 0
        inputs = []
        for key , value in self.utxo.items():
            utxo = value
            total += utxo.value 
            inputs.append(TransactionInput(utxo.id , utxo))
            if(total > value_sent):
                break

        #Pass "0" as default argument
        new_transaction = Transaction("0", self.publicKey, reciepient, value_sent, inputs)
        new_transaction.generate_signature(self.privateKey)  

        for obj in inputs:
            self.utxo.pop(obj.transaction_output_id)

        return new_transaction 

class LoadWallet(Wallet):
    def __init__(self , privatekey , publicKey):
        self.privateKey = privatekey
        self.publicKey = publicKey
        self.utxo = {}
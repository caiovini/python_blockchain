import json
import sys

from constants import constants as const
from objects.block import Block
from objects.block import LoadBlock
from objects.wallet import Wallet
from objects.wallet import LoadWallet
from objects.transaction import Transaction
from objects.transaction import TransactionOutput
from objects.transaction import TransactionInput
from objects.transaction import LoadTransactions
from objects.transaction import LoadTransactionOutput
from ellipticcurve.publicKey import PublicKey
from ellipticcurve.privateKey import PrivateKey
from util.string import String

blockchain = []
main_utxo = {}

def main():

    
    WalletA = Wallet()
    WalletB = Wallet()
    WalletC = Wallet()
    generate_genesis_block(WalletA)
    
    block = Block("Hi I am a block " + str(len(blockchain)) , blockchain[len(blockchain) - 1].hash)
    print("\nWalletA's balance is: " + str(WalletA.get_balance(main_utxo)))
    print("\nWalletA is Attempting to send funds 40 to WalletB...")
    if(block.add_transaction(WalletA.send_funds(
        WalletB.publicKey, 40, main_utxo), main_utxo)):
        add_block(block)
        print("\nWalletA's balance is: " + str(WalletA.get_balance(main_utxo)))

    block = Block("Hi I am a block " + str(len(blockchain)) , blockchain[len(blockchain) - 1].hash)
    print("\nWalletB's balance is: " + str(WalletB.get_balance(main_utxo)))
    print("\nWalletB is Attempting to send funds 40 to WalletA...")
    if(block.add_transaction(WalletB.send_funds(
        WalletA.publicKey, 40, main_utxo), main_utxo)):
        add_block(block)
        print("\nWalletB's balance is: " + str(WalletB.get_balance(main_utxo)))

    block = Block("Hi I am a block " + str(len(blockchain)) , blockchain[len(blockchain) - 1].hash)
    print("\nWalletA's balance is: " + str(WalletA.get_balance(main_utxo)))
    print("\nWalletA is Attempting to send funds 20 to WalletC...")
    if(block.add_transaction(WalletA.send_funds(
        WalletC.publicKey, 20, main_utxo), main_utxo)):
        add_block(block)
        print("\nWalletC's balance is: " + str(WalletC.get_balance(main_utxo)))
        print("\nWalletA's balance is: " + str(WalletA.get_balance(main_utxo)))    
            

    if(is_chain_valid()):
        print("Blockchain is valid")

def is_chain_valid():
    hash_target = String.get_dificulty_string(const.DIFFICULTY)

    for i in range(1, len(blockchain)):
        current_block = blockchain[i]
        previous_block = blockchain[i - 1]

        if(current_block.hash != current_block.calculate_hash()):
            print("Current Hashes not equal")
            return False

        if(previous_block.hash != previous_block.calculate_hash()):
            print("Previous Hashes not equal")
            return False

        if(current_block.hash[:const.DIFFICULTY] != hash_target):
            print("This block hasn't been mined")
            return False               

    return True


def add_block(new_block):
    new_block.mine_block(const.DIFFICULTY)
    blockchain.append(new_block)

def generate_genesis_block(WalletA):

    coinbase = Wallet()

    genesis = Transaction("0", coinbase.publicKey,
                          WalletA.publicKey, 100, None)
    genesis.generate_signature(coinbase.privateKey)
    genesis.outputs.append(TransactionOutput(
        genesis.transaction_id, genesis.reciepient, genesis.value))
    main_utxo[genesis.outputs[0].id] = genesis.outputs[0]

    print("Creating and Mining Genesis block... ")
    block = Block("Hi I am a block 0", "0")
    block.add_transaction(genesis, main_utxo)
    add_block(block)


if __name__ == "__main__":
    main()

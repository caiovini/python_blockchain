## python_blockchain
Small blockchain project written in python


This is a small blockchain written in python in which 3 wallets are created, WalletA creates and signs a transaction to WalletB, WalletB signs a new transaction to WalletA which sends funds to WalletC.

Each transaction is mined into a block applying sha256 algorithm.

For each wallet a public and a private key are created using an elliptic curve cryptography algorithm.

Reference project: https://medium.com/programmers-blockchain/create-simple-blockchain-java-tutorial-from-scratch-6eeed3cb03fa


![alt text](https://github.com/caiovini/python_blockchain/blob/master/Mining.png)


## Instructions

install requirements :

pip3 install -r requirements.txt

init application:

python3 noob_chain.py
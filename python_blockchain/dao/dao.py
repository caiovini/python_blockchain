

import sqlite3
from pathlib import Path


class DAO():
    def __init__(self, db_file):
        self.con = self.check_file_exists(db_file)

    def check_file_exists(self, db_file):
        file = Path(db_file)
        if(file.is_file() == False):
            try:
                con = sqlite3.connect(db_file)
                cursor = con.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS TB_BLOCK
                    ( BLOCK_ID INTEGER PRIMARY KEY AUTOINCREMENT ,
                      DATA TEXT NOT NULL,
                      PREVIOUS_HASH TEXT NOT NULL,
                      TIME_STAMP TEXT NOT NULL,
                      NONCE INTEGER NOT NULL,
                      HASH TEXT NOT NULL)""")
                con.commit()      

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS TB_TRANSACTION
                    ( ID_TRANS INTEGER PRIMARY KEY AUTOINCREMENT,
                      TRANSACTION_ID TEXT NOT NULL ,
                      BLOCK_ID INTEGER NOT NULL,
                      SENDER TEXT NOT NULL,
                      RECIEPIENT TEXT NOT NULL,
                      VALUE DOUBLE NOT NULL,
                      SEQUENCE INTEGER NOT NULL ,
                      FOREIGN KEY (BLOCK_ID) REFERENCES TB_BLOCK (BLOCK_ID) ON DELETE CASCADE ON UPDATE NO ACTION); """)
                con.commit()      

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS TB_OUTPUTS
                    ( ID_OUTPUT INTEGER PRIMARY KEY AUTOINCREMENT,
                      PARENT_TRANSACTION_ID TEXT NOT NULL ,
                      RECIEPIENT TEXT NOT NULL,
                      VALUE DOUBLE NOT NULL,
                      ID TEXT NOT NULL ,
                      FOREIGN KEY (PARENT_TRANSACTION_ID) REFERENCES TB_TRANSACTION (TRANSACTION_ID) ON DELETE CASCADE ON UPDATE NO ACTION); """)
                con.commit()      

                cursor.execute("CREATE TABLE IF NOT EXISTS TB_WALLET( PRIVATE_KEY TEXT NOT NULL, PUBLIC_KEY TEXT NOT NULL );")      
                con.commit()

                return con

            except Exception as err:
                print(err)
                return None
        else:
            return sqlite3.connect(db_file)        

    def close_connection(self):
        self.con.close


class BlockchainDAO(DAO):
    def __init_(self, db_file):
        super().__init__(db_file)

    def record_to_db(self, blockchain , utxo):
        try:
            for block in blockchain:
                cursor = self.con.cursor()
                entities = (block.data, block.previous_hash,
                            block.time_stamp, block.nonce, block.hash)
                cursor.execute(
                    'INSERT INTO TB_BLOCK(DATA, PREVIOUS_HASH, TIME_STAMP, NONCE, HASH) VALUES (?, ?, ?, ?, ?)', entities)
                self.con.commit()

                cursor.execute('SELECT LAST_INSERT_ROWID()')
                block_id = cursor.fetchall()[0][0]  # Get last value inserted
                for transaction in block.transactions:
                    entities = (transaction.transaction_id, block_id, transaction.sender.toPem(
                    ), transaction.reciepient.toPem(), transaction.value, transaction.sequence)
                    cursor.execute(
                        'INSERT INTO TB_TRANSACTION(TRANSACTION_ID, BLOCK_ID, SENDER, RECIEPIENT, VALUE, SEQUENCE) VALUES (?, ?, ?, ?, ?, ?)', entities)
                    self.con.commit()

            for key , value in utxo.items():
                entities = (value.parent_transaction_id,
                            value.reciepient.toPem(), value.value, value.id)
                cursor.execute(
                    'INSERT INTO TB_OUTPUTS(PARENT_TRANSACTION_ID, RECIEPIENT, VALUE, ID) VALUES (?, ?, ?, ?)', entities)
                self.con.commit()

        except Exception as err:
            print(err)

    def load_data(self):
        try:
            cursor = self.con.cursor()
            cursor.execute("""

            SELECT BL.* , TR.* , OU.*
               FROM TB_BLOCK BL
  
            INNER JOIN TB_TRANSACTION TR
               ON TR.BLOCK_ID = BL.BLOCK_ID
    
            INNER JOIN TB_OUTPUTS OU
               ON OU.PARENT_TRANSACTION_ID = TR.TRANSACTION_ID
    
             ORDER BY BL.BLOCK_ID""")

            return cursor.fetchall()

        except Exception as err:
            print(err)

    def close_connection(self):
        self.con.close()


class WalletDAO(DAO):
    def __init_(self, db_file):
        super().__init__(db_file)

    def record_to_db(self, privatekey , publickey):
        
        cursor = self.con.cursor()
        entities = (privatekey.toPem() , publickey.toPem())
        cursor.execute(
            "INSERT INTO TB_WALLET VALUES (? , ?)", entities)
        self.con.commit()

    def load_data(self):
        try:
            cursor = self.con.cursor()
            cursor.execute("SELECT * FROM TB_WALLET")

            return cursor.fetchall()

        except Exception as err:
            print(err)

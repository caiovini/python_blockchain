
from util.string import String


class TransactionOutput():
    def __init__(self, parent_transaction_id, reciepient, value):
        self.parent_transaction_id = parent_transaction_id
        self.reciepient = reciepient
        self.value = value
        self.id = String.apply_sha256(
            String.get_string_from_key(reciepient) + str(value) + parent_transaction_id)

    def is_mine(self, publicKey):
        return publicKey.toPem() == self.reciepient.toPem()


class TransactionInput():
    def __init__(self, transaction_output_id, transaction_output):
        self.transaction_output_id = transaction_output_id
        self.utxo = transaction_output


class Transaction():
    def __init__(self, transaction_id, sender, reciepient, value, inputs):
        self.transaction_id = transaction_id
        self.sender = sender
        self.reciepient = reciepient
        self.value = value
        self.inputs = inputs
        self.outputs = []
        self.sequence = 0

    def process_transaction(self, main_utxo):
        if(self.verify_signature() == False):
            print("Transaction signature failed to verify")
            return False

        for obj in self.inputs:
            obj = main_utxo[obj.transaction_output_id]

        left_over = self.get_inputs_value() - self.value        
        self.transaction_id = self.calculate_hash()
        self.outputs.append(TransactionOutput(
            self.transaction_id, self.reciepient, self.value))
        self.outputs.append(TransactionOutput(
            self.transaction_id, self.sender, left_over))

        for obj in self.outputs:
            main_utxo[obj.id] = obj

        for obj in self.inputs:
            if(obj.utxo == None):
                continue

            main_utxo.pop(obj.utxo.id)

        return True

    def get_inputs_value(self):
        total = 0
        for obj in self.inputs:
            if (obj.utxo == None):
                continue
            total += obj.utxo.value
        return total

    def generate_signature(self, privatekey):
        data = String.get_string_from_key(
            self.sender) + String.get_string_from_key(self.reciepient) + str(self.value)
        self.signature = String.apply_ecdsas(privatekey, data)

    def verify_signature(self):
        data = String.get_string_from_key(
            self.sender) + String.get_string_from_key(self.reciepient) + str(self.value)
        return String.verify_ecdsas(data, self.signature , self.sender)  

    def get_outputs_value(self):
        total = 0
        for obj in self.outputs:
            total += obj.value
        return total    

    def calculate_hash(self):
        self.sequence += 1
        return String.apply_sha256(
               String.get_string_from_key(self.sender) +
               String.get_string_from_key(self.reciepient) +
               str(self.value) +
               str(self.sequence)
           )   

class LoadTransactions(Transaction):
    def __init__(self, transaction_id, sender, reciepient, value, inputs , outputs , sequence):
        self.transaction_id = transaction_id
        self.sender = sender
        self.reciepient = reciepient
        self.value = value
        self.inputs = inputs
        self.outputs = outputs
        self.sequence = sequence                  

class LoadTransactionOutput(TransactionOutput):
    def __init__(self, parent_transaction_id, reciepient, value, id):
        self.parent_transaction_id = parent_transaction_id
        self.reciepient = reciepient
        self.value = value
        self.id = id

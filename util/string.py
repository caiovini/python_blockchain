import base64

from ellipticcurve.ecdsa import Ecdsa
from hashlib import sha256 as h


class String:

    def apply_sha256(input_str):
        # Returns hash in hexadecimal
        return h(input_str.encode()).hexdigest()

    def get_dificulty_string(difficulty=1):

        # Returns string of zeroes according to difficulty
        output = ""
        for x in range(difficulty):
            output += "0"

        return output

    def apply_ecdsas(privateKey, input):
        return Ecdsa.sign(input, privateKey)

    def verify_ecdsas(input, signature, publicKey):
        return Ecdsa.verify(input, signature, publicKey)

    def get_string_from_key(key):
        #This function by itself is returning bytes
        return str(base64.b64encode(key.toPem().encode('utf-8')))

    def get_merkle_root(transactions):
        count = len(transactions)
        previous_tree_layer = []
        for obj in transactions:
            previous_tree_layer.append(obj.transaction_id)

        tree_layer = previous_tree_layer
        while(count > 1):
            tree_layer = []
            for i in range(1, len(previous_tree_layer), 2):
                tree_layer.append(apply_sha256(
                    previous_tree_layer[i - 1]) + previous_tree_layer[i])

            count = len(tree_layer)
            previous_tree_layer = tree_layer

        if(len(tree_layer) == 1):
            return tree_layer[0]
        else:
            return ""

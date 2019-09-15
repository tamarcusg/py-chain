from collections import OrderedDict
import json
import hashlib
import requests


class Blockchain:

    def __init__(self):
        # self.name = name
        self.chain = []
        self.current_transactions = []
        # self.nodes = set()

        self.add_new_block(previous_hash='1')

    def add_transaction(self, transaction):
        self.current_transactions.append(transaction)
        if (len(self.current_transactions) == 3):
            self.add_new_block(self.hash(self.last_block))
            self.current_transactions = []

    def add_new_block(self, previous_hash):
        block = OrderedDict()
        block['index'] = len(self.chain) + 1
        block['transactions'] = self.current_transactions
        block['previous_hash'] = previous_hash

        self.current_transactions = []
        self.chain.append(block)
        return block

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block).encode()
        return hashlib.sha256(block_string).hexdigest()



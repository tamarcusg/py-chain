from collections import OrderedDict
import json
import hashlib
from flask import Flask, jsonify, request
import requests
import random
from uuid import uuid4

class Blockchain:

    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.new_block(previous_hash='1')

    def new_block(self, previous_hash):
        block = OrderedDict()
        block['index'] = len(self.chain) + 1
        block['transactions'] = self.current_transactions
        block['previous_hash'] = previous_hash

        self.current_transactions = []
        self.chain.append(block)
        return block
    
    @staticmethod
    def hash(block):
        block_string = json.dumps(block).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]
    
    def new_transaction_breed(self, user_1_address, user_2_address, user_1_genome, user_2_genome, new_genome_1, new_genome_2) :
        self.current_transactions.append({
            'type' : "breed",
            'user_1_address' : user_1_address,
            'user_2_address' : user_2_address,
            'user_1_genome' : user_1_genome,
            'user_2_genome' : user_2_genome,
            'new_genome_1' : new_genome_1,
            'new_genome_2' : new_genome_2
        })
		
        return {'index' : self.last_block['index'] + 1, 'type' : "breed", 'user_1_address' : user_1_address, 'user_2_address' : user_2_address,
            'user_1_genome' : user_1_genome, 'user_2_genome' : user_2_genome, 'new_genome_1' : new_genome_1, 'new_genome_2' : new_genome_2}
    
    
    def new_transaction_create(self, user_address) :
        genome = random.randint(1,1001)
        self.current_transactions.append({
            'type' : "create",
            'user_address' : user_address,
            'genome' : genome
        })
    	
        return {'index' : self.last_block['index'] + 1, 'type' : "create", 'user_address' : user_address, 'genome' : genome}
    
  

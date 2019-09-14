from collections import OrderedDict
import json
import hashlib
from flask import Flask, jsonify, request
import requests
import random
from uuid import uuid4
from blockchain import Blockchain

app = Flask(__name__)
list_identified = str(uuid4()).replace('-', '')
blockchain = Blockchain()
    
@app.route('/transactions/new/breed', methods=['POST'])
def new_transaction_breed():
    values = request.get_json()
      
    required = ['type', 'user_1_address', 'user_2_address', 'user_1_genome', 'user_2_genome']
    if not all(k in values for k in required):
        return 'Missing values', 400
      
    new_genome_1 = (values['user_1_genome'] +  values['user_2_genome'] / 2) + random.randint(1, 51)
    new_genome_2 = (values['user_1_genome'] +  values['user_2_genome'] / 2) + random.randint(1, 51)
      
    response = blockchain.new_transaction_breed(values['user_1_address'], values['user_2_address'], values['user_1_genome'], values['user_2_genome'],
        new_genome_1, new_genome_2)
    
    return jsonify(response), 200
    
@app.route('/transactions/new/create', methods=['POST'])
def new_transaction_create():
    values = request.get_json()
      
    required = ['type', 'user_address']
      
    if not all(k in values for k in required):
      return 'Missing values', 400
      
    response = blockchain.new_transaction_create(values['user_address'])
    
    return jsonify(response), 201
    
@app.route('/mine', methods=['GET'])
def mine() :
    last_block = blockchain.last_block
    #proof = blockchain.proof_of_work(last_block)
      
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(previous_hash)
      
    response = {
      'message' : 'New Block Forged',
      'index' : block['index'],
      'transactions' : block['transactions'],
      'prev_hash' : block['previous_hash'],
    }
      
    return jsonify(response), 200
    
    
@app.route('/chain', methods=['GET'])
def full_chain() :
    response = {
      'chain' : blockchain.chain,
      'length' : len(blockchain.chain)
    }
    return jsonify(response), 200
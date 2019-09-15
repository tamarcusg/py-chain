from collections import OrderedDict
import json
import hashlib
from flask import Flask, jsonify, request
import requests
import random
from uuid import uuid4
from blockchain import Blockchain
from nodes import Nodes

nodeNames = {
  'Anirudh': 'http://192.168.0.23:5000',
  # 'Martin': 'http://192.168.0.9:5001',
  'Tamarcus': 'http://192.168.0.29:5002'
}

app = Flask(__name__)
list_identified = str(uuid4()).replace('-', '')
blockchain = Blockchain("Anirudh")
nodes = Nodes()
    
@app.route('/transactions/new/breed', methods=['POST'])
def new_transaction_breed():
    values = request.get_json()
      
    required = ['type', 'user_1_address', 'user_2_address', 'user_1_genome', 'user_2_genome']
    if not all(k in values for k in required):
        return 'Missing values', 400

    if values['user_1_address'] == values['user_2_address'] :
        return 'Same user', 400
      
    new_genome_1 = (values['user_1_genome'] +  values['user_2_genome'] / 2) + random.randint(1, 51)
    new_genome_2 = (values['user_1_genome'] +  values['user_2_genome'] / 2) + random.randint(1, 51)
      
    response = blockchain.new_transaction_breed(values['user_1_address'], values['user_2_address'], values['user_1_genome'], values['user_2_genome'],
        new_genome_1, new_genome_2)

    nodes.push_transaction(response)
    
    return jsonify(response), 200
    
@app.route('/transactions/new/create', methods=['POST'])
def new_transaction_create():
    values = request.get_json()
      
    required = ['type', 'user_address']
      
    if not all(k in values for k in required):
      return 'Missing values', 400
      
    response = blockchain.new_transaction_create(values['user_address'])

    nodes.push_transaction(response)
    
    return jsonify(response), 201
    
@app.route('/mine', methods=['GET'])
def mine() :
    last_block = blockchain.last_block
    #proof = blockchain.proof_of_work(last_block)
      
    previous_hash = blockchain.hash(last_block)
    block = blockchain.add_new_block(previous_hash)
      
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


@app.route('/')
def hello_world():
    address = request.remote_addr
    person = ''
    if address == '192.168.0.29':
        person = 'Tamarcus'
    if address == '192.168.0.23':
        person = 'Anirudh'
    if address == '192.168.0.9':
        person = 'Martin'
    response = 'Welcome to the Chain ' + person
    return response


@app.route('/getChain')
def get_chain():
    response = {"Full Chain" : blockchain.chain}
    return jsonify(response), 200


@app.route('/addBlock')
def add_block():
    blockchain.add_new_block(blockchain.hash(blockchain.last_block))
    for node, address in nodeNames.items():
        if (node==blockchain.name):
            continue
        requests.get(address + '/chainUpdated')
    response = {"Block Added" : blockchain.last_block}
    return jsonify(response), 200


@app.route('/addTransaction')
def add_transaction():
    blockchain.add_transaction("Testing 123")
    if (len(blockchain.current_transactions) == 3):
        add_block()
        blockchain.current_transactions = []
    response = "Added Transaction"
    return jsonify(response), 200


@app.route('/resolveChain')
def resolve_chain(address):
    person = ''
    if address == '192.168.0.29':
        person = 'Tamarcus'
    if address == '192.168.0.23':
        person = 'Anirudh'
    if address == '192.168.0.9':
        person = 'Martin'
    destination = nodeNames[person]
    response = requests.get(destination + '/getChain').json()
    foreign_chain = response["Full Chain"]
    if len(foreign_chain) > len(blockchain.chain):
        blockchain.chain = foreign_chain
    return jsonify("Foreign Chain is Longer, Updating Local Chain..."), 200


@app.route('/chainUpdated')
def call_resolve_chain():
    address = request.remote_addr
    resolve_chain(address)
    return jsonify("Received Chain Update Notification...Will Resolve"), 200
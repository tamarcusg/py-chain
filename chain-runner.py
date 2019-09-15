from blockchain_basic import Blockchain
from flask import Flask, jsonify, request
import requests
import json

nodes = {
  'Anirudh': 'http://192.168.0.23:5000',
  'Martin': 'http://192.168.0.9:5001'
  # 'Tamarcus': 'http://192.168.0.29:5002'
}

chain1 = Blockchain()


app = Flask(__name__)

@app.route('/')
def hello_world():
    address = request.remote_addr
    person = ''
    if (address=='192.168.0.29'):
        person = 'Tamarcus'
    response = 'Welcome to the Chain ' + person + '\n' + \
               'Call /getChain for current blockchain' + '\n'
    return response

@app.route('/getChain')
def get_chain():
    response = {"Full Chain" : chain1.chain}
    return jsonify(response), 200

@app.route('/addBlock')
def add_block():
    chain1.add_new_block(chain1.hash(chain1.last_block))
    # for node, address in nodes.items():
    #     if (node==chain1.name):
    #         continue
    #     requests.get(address + '/chainUpdated')
    response = {"Block Added" : chain1.last_block}
    return jsonify(response), 200


@app.route('/addTransaction')
def add_transaction():
    chain1.add_transaction("Testing 123")
    response = "Added Transaction"
    return jsonify(response), 200

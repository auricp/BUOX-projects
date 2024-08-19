# imports
import hashlib
import json
from time import time
from uuid import uuid4
from textwrap import dedent

from flask import Flask, jsonify, request

# blockchain Class
class Blockchain(object):
    
    # creates two empty lists. One to store the blockchain, and another to store transactions
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
    
    '''
    -----------------------------------------------
    BASIC METHODS OF THE CLASS
    -----------------------------------------------
    '''
    
    def new_block(self, proof, previous_hash=None):
        '''
        Creates a new block and adds it to the chain
        
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Has of the previous Block
        
        :return: <dict> New Block
        '''
        
        # Note: Blocks are 1-indexed
        # self.hash(self.chain[-1]) is for the first block (genesis block) when previous_hash isnt provided
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        
        self.current_transactions = []
        self.chain.append(block)
        return block
    
    
    def new_transaction(self, sender, recipient, amount):
        '''
        Adds a new transaction to the current transactions list
        
        :param sender: <str> Address of the Sender
        :param recipient <str> Address of the Recipient
        :param amount: <int> Amount
        
        :return: <int> The index of the Block that will hold this transaction 
        '''
        
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        
        return self.last_block['index'] + 1
    
    
    def proof_of_work(self,last_proof):
        '''
        Simple Proof of Work Algorithm:
        - Find a number p' such that hash(pp') contains 4 leading zeros
        - p is the previous proof, and p' is the new proof
        
        :param last_proof: <int>
        :return: <int>
        '''
        
        proof = 0
        while not self.valid_proof(last_proof,proof):
            proof += 1
            
        return proof


    @staticmethod
    def valid_proof(last_proof,proof):
        '''
        Validates the Proof: Does hash(last_proof,proof) contain 4 leading zeros?
        
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        
        :return: <bool> True if correct, False if not
        '''
        
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'
    
    
    # property decorator means the method acts like an attribute
    @property
    def last_block(self):
        '''
        Returns the last block in the blockchain
        '''
        
        return self.chain[-1]
    
    
    # staticmethod decorator means it cant access the class attributes (security) and can return an object of the class
    @staticmethod
    def hash(block):
        '''
        Creates a SHA-256 hash of a Block
        
        :param block: <dict> Block
        
        :return: <str>
        '''
        
        # have to order the dictionary for consistent hashing
        # dumps serializes an object to a json formatted str
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

'''
-----------------------------------------------
API SETUP FOR THE BLOCKCHAIN USING FLASK
-----------------------------------------------
'''

# Instantiate our Node
app = Flask(__name__)

# generate a unique address (globally unique) for this node
node_identifier = str(uuid4()).replace('-','')

# Instantiate the Blockchain
blockchain = Blockchain()

# init genesis block
blockchain.new_block(previous_hash='1',proof=100)

# method to mine a new block
@app.route('/mine', methods=['GET'])
def mine():
    # Run the proof of work algo to get the next proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    
    # must recieve a reward for finding the proof
    # the sender is "0" to signify that this node has mined a new coin
    blockchain.new_transaction(
        sender='0',
        recipient=node_identifier,
        amount=1,
    )
    
    # forge the new block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    
    response = {
        'message': 'New Block Forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    
    return jsonify(response), 200


# method to create a new transaction
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    
    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing Values', 400
    
    # Create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


# method to return the whole blockchain
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


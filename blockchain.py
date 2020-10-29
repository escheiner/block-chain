#!/usr/bin/python3
from hashlib import sha256
import json 
import time

class Block: 
    def __init__(self, index, transactions, timestamp):
        """
        Creates a constructur for the Block class
        index = unique id of the block 
        transaction = list of transactions
        timestamp = time of generation of the block 
        previous_hash = hash of the previous block in the chain
        """
        self.index = index 
        self.transactions = transactions
        self.timestamp = timestamp 
        self.previous_hash = previous_hash
 
    def compute_hash(block):
        """
        Returns hash of the block by first converting it into a json string 
        """
        block_string = json.dumps(self.__dict__, sort_keys= True)
        return sha256(block_string.encode()).hexdigest()  

class Blockchain:
    #difficulty of proof of work algorithm
    difficulty = 2 
  
    def __init__(self):
        """
        Constructor for the blockchain class
        """
        self.unconfirmed_transactions = [] 
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        a function that creates a genesis block that appends it to the chain, the block has index 0 previous hash 0 and a valid hash.
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        """
        a quick way to retriece the last block in the chain. The chain will always contain one block 
        """
        return self.chain[-1]

    def proof_of_work(self, block):
        """
        Function tries different values of the nonce to get a hash that satisfies our difficulty criteria
        """
        block.nonce = 0 
        computed_hash = block.compute_hash()
        while not computed_hash.starswith('0' * Blockchain.difficulty):
            block.nonce += 1 
            computed_hash = block.compute_hash()
   
    def add_block(self, block, proof):
        """ 
        Function that adds the block to the chain after verification 
        this includes : 
        1) Checking if the proof is valid 
        2) the previous hash referred in the block, and the hash of a latest block in the chain match
        """
        previous_hash = self.last_block.hash
       
        if previous_hash != block.previous: 
            return False
    
        if not Blockchain.is_valid_proof(block, proof):
            return False
        
        block.hash = proof 
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash): 
        """ 
         Check if block hash is a valid hash of block and satisfies the difficulty criteria
        """ 
        return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == compute_hash()) 

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self): 
        """
        This function is an interface to add the pending transactions to the blockchain by adding them to the block and figuring out proof of work
        """
        if not self.unconfirmed_transactions: 
            return False
       
        last_block = self.last_block
  
        new_block = Block(index= last_block.index + 1, 
                          transactions = self.unconfirmed_transactions,
                          timestamp = time.time(),
                          previous_hash = last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index


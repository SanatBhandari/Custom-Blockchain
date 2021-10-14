# Import all the necessary packages
import hashlib
import json
import random
import binascii
import pandas as pd
import pylab as pl
import logging
import string
import collections
import Crypto
import Crypto.Random

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from time import time

class Blockchain(object):
  def __init__(self):
    """ Constructor for the blockchain object
    Parameters
    ----------
    Requires no parameters

    Returns
    -------
    Blockchain object
    """
    self.chain = []
    self.pending_transactions = []
    self.completed_transactions = []
    self.genesis()

    self.new_block(previous_hash="The greatest blockchain ever", proof=100)

  
  def genesis(self):
    return self.new_block(0)


  def new_block(self, proof, previous_hash=None):
    """ Create a new block in the blockchain
    Parameters
    ----------
    proof: Proof of the blockchain
    previous_hash: Hash for the previous block

    Returns
    -------
    Blockchain object
    """
    block = {
        'index': len(self.chain) + 1,
        'timestamp': time(),
        'transactions': self.pending_transactions,
        'proof': proof,
        'previous_hash': previous_hash or self.hash(self.chain[-1])
    }

    self.pending_transactions = []
    self.chain.append(block)

    return block
  

  @property
  def last_block(self):
    """ Return the last block in the blockchain
    Parameters
    ----------
    Requires no parameters

    Returns
    -------
    Blockchain object
    """
    return self.chain[-1]


  def is_it_valid(block, prev_block):
    if prev_block.index + 1 != block.index:
      return False

    elif prev_block.calculate_hash() != block.prev_hash:
      return False

    elif block.timestamp <= prev_block.timestamp:
      return False


  def new_transaction(self, sender, recipient, amount):
    """ Create a new transction in the block
    Parameters
    ----------
    sender: The sender's address
    recipient: The recipient's address
    amount: The amount to be sent

    Returns
    -------
    The previous block to which the index will be added
    """
    transaction = {
        'sender': sender, 
        'recipient': recipient, 
        'amount': amount
    }

    self.pending_transactions.append(transaction)
    return self.last_block['index'] + 1


  def hash(self, block):
    """ Hash function
    Parameters
    ----------
    block: The block to be hashed

    Returns
    -------
    Hash for the block
    """
    string_object = json.dumps(block, sort_keys=True)
    block_string = string_object.encode()

    raw_hash = hashlib.sha256(block_string)
    hex_hash = raw_hash.hexdigest()

    return hex_hash

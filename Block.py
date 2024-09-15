import hashlib
from helper import *
from io import BytesIO

class Block_header:
    def __init__(self, version, pre_block, merkle_root, timestamp, bits, nonce):
        self.version = version
        self.pre_block = pre_block
        self.merkle_root = merkle_root # transaction hash
        self.timestamp = timestamp
        self.bits = bits # target 
        self.nonce = nonce # the PoW random number

    @classmethod
    def parse(cls, s):
        s = BytesIO(s)
        version = little_endian_to_int(s.read(4))
        pre_block = s.read(32)[::-1]
        merkle_root = s.read(32)[::-1]
        timestamp = little_endian_to_int(s.read(4))
        bits = s.read(4)
        nonce = s.read(4)
        return cls(version, pre_block, merkle_root, timestamp, bits, nonce)
    
    def print_task(self):
        print("version: %s" %self.version)
        print("pre_block: %s" % self.pre_block)
        print("merkle_root: %s" %self.merkle_root)
        print("timestamp: %s" %self.timestamp)
        print("bits: %s" %self.bits)
        print("difficulty: %s" %self.difficulty())

    def print(self):
        print("version: %s" %self.version)
        print("pre_block: %s" % self.pre_block)
        print("merkle_root: %s" %self.merkle_root)
        print("timestamp: %s" %self.timestamp)
        print("bits: %s" %self.bits)
        print("nonce: %s" %self.nonce)

    def serialize(self):
        result = int_to_little_endian(self.version, 4)
        result += self.pre_block[::-1]
        result += self.merkle_root[::-1]
        result += int_to_little_endian(self.timestamp, 4)
        result += self.bits
        result += self.nonce
        return result

    def hash(self):
        s = self.serialize()
        sha = hashlib.sha256(s).digest()
        return sha[::-1]
    
    def target(self):
        bits = self.bits
        exponent = bits[-1]
        coefficient = little_endian_to_int(bits[:-1])
        target = coefficient * 256 ** (exponent - 3)
        return target

    def difficulty(self):
        lowest = 0xffff * 256**(0x1d - 3)
        return lowest / self.target()
    
    def check_pow(self):
        sha = self.hash()
        proof = little_endian_to_int(sha)
        return proof < self.target()
        

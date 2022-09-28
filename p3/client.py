import math
import socket
import sys

import pyDHE

host = "127.0.0.1"
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    
    bob = pyDHE.new(14)
    bob_pub_key = bob.getPublicKey()
    bob_pub_key_bytes = bob_pub_key.to_bytes(math.ceil(bob_pub_key.bit_length()/8), sys.byteorder, signed=False)
    s.sendall(bob_pub_key_bytes)
    alice_pub_key_bytes = s.recv(2048)
    alice_pub_key = int.from_bytes(alice_pub_key_bytes, sys.byteorder, signed=False)
    shared_key = bob.update(alice_pub_key)
    print(hex(shared_key))
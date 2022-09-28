import math
from socket import socket, AF_INET, SOCK_STREAM
import sys
import pyDHE

myClientSocket = socket(AF_INET, SOCK_STREAM)

myClientSocket.connect(('localhost', 12345))

bob = pyDHE.new(14)
bob_pub_key = bob.getPublicKey()
bob_pub_key_bytes = bob_pub_key.to_bytes(math.ceil(bob_pub_key.bit_length()/8), sys.byteorder, signed=False)
myClientSocket.sendall(bob_pub_key_bytes)

alice_pub_key_bytes = myClientSocket.recv(2048)
alice_pub_key = int.from_bytes(alice_pub_key_bytes, sys.byteorder, signed=False)
shared_key = bob.update(alice_pub_key)

print(hex(shared_key))
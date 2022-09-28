from email.headerregistry import Address
import math
from multiprocessing import connection
import socket
import sys

import pyDHE

host = "127.0.0.1"
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()

    while True:
        connection, address = s.accept()

        with connection:
            print("Connection by", address)

            alice = pyDHE.new(14)
            bob_pub_key_bytes = connection.recv(2048)
            bob_pub_key = int.from_bytes(bob_pub_key_bytes,sys.byteorder, signed=False)
            shared_key = alice.update(bob_pub_key)
            alice_pub_key = alice.getPublicKey()
            alice_pub_key_bytes = alice_pub_key.to_bytes(math.ceil(alice_pub_key.bit_length()/ 8), sys.byteorder, signed=False)
            connection.sendall(alice_pub_key_bytes)
            print(hex(shared_key))
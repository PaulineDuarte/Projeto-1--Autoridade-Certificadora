
import math
from multiprocessing import connection
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import sys

import pyDHE


def HandleRequest(mClientSocket, mClientAddr):
    while True:
        # Este loop foi criado para que o servidor conseguisse receber diversas requisições de
        # um mesmo cliente, usando a mesma conexão, ou seja, sem que fosse necessária a
        # criação de uma nova conexão.
        print('Esperando o próximo pacote ...')
        # Recebendo os dados do Cliente:
        # o Servidor irá receber bytes do cliente, sendo necessária a conversão de bytes
        # para string ou para o tipo desejado.
        data = mClientSocket.recv(2048)
        print(f'Requisição recebida de {mClientAddr}')
        req = data.decode()
        print(f'A requisição foi:{req}')
        # Após receber e processar a requisição o servidor está apto para enviar uma resposta.
        rep = 'Hey cliente!'
        mClientSocket.send(rep.encode())

mSocketServer = socket(AF_INET, SOCK_STREAM)
print(f'Socket criado ...')
#Passo 2: Transformando o socket em um socket servidor.
#Dar Bind significa vincular um socket a um endereço
mSocketServer.bind(('127.0.0.1',12345))
#Colocar o servidor para escutar as solicitações de conexão
mSocketServer.listen()

while True:
    connection, address = mSocketServer.accept()

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
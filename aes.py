from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time
import hashlib


class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".aes", 'wb') as fo:
            fo.write(enc)
        

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open( "dec"+file_name[:-4], 'wb') as fo:
            fo.write(dec)
       

   
                       
def key_generator(password):
    password = password.encode()
    key = hashlib.sha256(password).digest()
    enc= Encryptor(key)
    return enc
    

while True:
    choice = int(input(
            "1.encrypt file.\n2.decrypt file.\n3.exit.\n"))
    
    if choice == 1:
        password = input("Enter the password to encrypt the file. Remember the password as the same should be used to decrypt this file: ")
        enc = key_generator(password)
        enc.encrypt_file(str(input("Enter name of file to encrypt: ")))
    elif choice == 2:
        password = input("Enter the password to decrypt the file: ")
        enc = key_generator(password)
        enc.decrypt_file(str(input("Enter name of file to decrypt: ")))    
    elif choice == 3:
        exit()
    else:
        print("Please select a valid option!")



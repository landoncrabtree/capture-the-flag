#!/usr/local/bin/python
import time
import base64 as b64
from pwn import xor

def epochrypt(enc):
    bits = bytes([(b + 3) % 256 for b in enc])
    based = b64.b64encode(bits)
    epc = str(int(time.time())).encode()
    final = xor(based, epc)
    print(final.hex())


def menupage():
    print("Epochrypt v1.0")
    print("\"The Dynamic Encryption Method\"")
    print("------------------------------------")
    print("1. Encrypt Text")
    print("2. View Encrypted Flag")
    print("3. Check Flag")
    print("4. Exit Program")


try:
    while True:
        menupage()
        option = input("Enter option here: ")
        if option == "1":
            textToEncrypt = input("Enter String: ")
            epochrypt(textToEncrypt.encode())
            exit(0)
        if option == "2":
            with open("/app/flag.txt", "rb") as file:
                flag = file.read()
            epochrypt(flag)
            exit(0)
        if option == "3":
            checkFlag = input("Enter flag here to check: ")
            with open("/app/flag.txt", "rb") as file:
                flag = file.read()
                if flag in (checkFlag + "\n").encode():
                    print("Correct! You got it, now go submit that thang.")
                    exit(0)
                else:
                    print("*BUZZ* That ain't it bud :(")
                    exit(0)
        if option == "4":
            print("bye bye!")
            exit(0)

except KeyboardInterrupt:
    print("CTRL + C detected, Quitting program...")
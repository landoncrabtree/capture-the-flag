import random
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes, inverse
import hashlib

bit_length = 128
p = getPrime(bit_length)
q = getPrime(bit_length)
r = getPrime(bit_length)

N = p * q * r

e1 = 3
e2 = 5

def nested_encrypt(message, e1, e2, N):
    msg_num = bytes_to_long(message)
    step1 = pow(msg_num, e1, N)
    salt = (p + q)  
    step2 = (step1 + salt) % N
    step3 = pow(step2, e2, N)
    mask = int(hashlib.sha256(long_to_bytes(step3)).hexdigest()[:8], 16) 
    ciphertext = step3 ^ mask
    return ciphertext

flag = b"csd{am_i_late_or_am_i_late}"
ciphertext = nested_encrypt(flag, e1, e2, N)
leak_p_bits = bin(p)[-64:]  
leak_q_bits = bin(q)[-64:]
partial_salt = (p + q) % 100000  

with open("public.txt", "w") as f:
    f.write(f"N = {N}\nLeaked bits of p = {leak_p_bits}\nLeaked bits of q = {leak_q_bits}\n")
    f.write(f"Partial salt (p + q mod 100000) = {partial_salt}\n")

with open("ciphertext.txt", "w") as f:
    f.write(str(ciphertext))

print("Try breaking me :)")
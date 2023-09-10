with open("MasonCompetitiveCyber2.txt", "r") as file:
    with open("output.txt", "w") as output:
        # used to clear output.txt
        pass
    for line in file:
        line = line.strip()
        m = line.count("M")
        a = line.count("a")
        s = line.count("s")
        o = line.count("o")
        n = line.count("n")
        c = line.count("C")
        with open("output.txt", "a") as output:
            output.write(str(m) + " " + str(a) + " " + str(s) + " " + str(o) + " " + str(n) + " " + str(c) + "\n")

import string
alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation + " "
with open("MasonCompetitiveCyber2.txt", "r") as f:
    unique = []
    for line in f:
        line = line.strip()
        for char in line:
            if char not in alphabet:
                unicode = ord(char)
                unicode_hex = str(hex(unicode))
                if unicode_hex not in unique:
                    unique.append(unicode_hex)
    print(str(unique) + "\n")

with open("MasonCompetitiveCyber2.txt", "r") as f:
    binary = ""
    for line in f:
        line = line.strip()
        for char in line:
            if char not in alphabet:
                unicode_hex = str(hex(ord(char)))
                if unicode_hex == "0x2062":
                    binary += "0"
                if unicode_hex == "0x2063":
                    binary += "1"
                if len(binary) == 8:
                    print(chr(int(binary, 2)), end="")
                    binary = ""
                    continue

import numpy as np
with open("output.txt", "r") as file:
    print("\n")
    for line in file:
        b = [5, 3, 8, 4, 7, 1]
        line = line.strip()
        line = line.split(" ")
        # convert to int
        line = [int(x) for x in line]
        product = np.dot(line, b)
        print(chr(product), end="")
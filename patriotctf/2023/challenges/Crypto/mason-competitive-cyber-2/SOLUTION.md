# Solution

Looking at `MasonCompetitiveCyber2.txt`, it appears to be a plaintext file. 

```
M⁢M⁣aa⁢a⁣a⁣ass⁢s⁢s⁣o‍o⁢o⁣n⁣C⁢CC⁣C⁣
M⁣aaaaaa⁣aa‍a⁢a⁣s⁣on⁣C⁢C⁣C⁢C⁣CCC‍C⁢C⁢C⁣C⁢CC
M⁢MM⁣a⁣sss⁣o‍oo⁢o⁣n⁣nCC⁣C⁢C⁢C⁣CC⁢CCCCC
M‍M⁢M⁣a⁣a⁢a⁢as⁣o⁢o⁣n‍n⁢CC⁢C⁣
```

The first intuition was to determine the occurence of each character. Assuming each line is a character of the flag, then:

```
M⁢M⁣aa⁢a⁣a⁣ass⁢s⁢s⁣o‍o⁢o⁣n⁣C⁢CC⁣C⁣ => P
M⁣aaaaaa⁣aa‍a⁢a⁣s⁣on⁣C⁢C⁣C⁢C⁣CCC‍C⁢C⁢C⁣C⁢CC => C
M⁢MM⁣a⁣sss⁣o‍oo⁢o⁣n⁣nCC⁣C⁢C⁢C⁣CC⁢CCCCC => T
M‍M⁢M⁣a⁣a⁢a⁢as⁣o⁢o⁣n‍n⁢CC⁢C⁣ => F
M⁢M‍M⁢M⁣M⁣M⁢M⁣Maaaa⁢ss⁢o⁢o‍oooo⁢o⁣onC⁣C⁢CCCC⁢CC⁢CC⁢C⁣CC‍CC⁢C⁣ => {
```

We can write a Python script to count the occurences for us:

```python
with open("MasonCompetitiveCyber2.txt", "r") as file:
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

# 2 5 4 3 1 4
# 1 10 1 1 1 13
# 3 1 3 4 2 12
# 3 4 1 2 2 13
# 8 4 2 8 1 16
# 4 9 1 1 1 11
```

However, we couldn't think of a way to convert these into the necessary ASCII for PCTF{. Looking at a hexdump of the file with `xxd MasonCompetitiveCyber2.txt`, we see that there are some non-printable characters in the file. 

![hexdump](https://i.imgur.com/rKU50tI.png)

We need to figure what all these characters are. 

```python
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
    print(unique)

# ['0x2062', '0x2063', '0x200d']
```

Looks like it's some sort of zero-width steganography. There's a great [tool](https://330k.github.io/misc_tools/unicode_steganography.html) that _usually_ works, but for this challenge it failed. It looks like they've implemented a different method of encoding. 

We'll need to write our own script to decode the zero-width characters. This took some trial and error to determine which character was 0, 1, or the separator. 

```python
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

# You're halfway there, now use these numbers to solve the rest: 5 3 8 4 7 1

```

So now we have a list of 6 numbers, and we know each line has 6 characters. We need to find a way to correlate 

```
2 5 4 3 1 4 & 5 3 8 4 7 1 => P
1 10 1 1 1 13 & 5 3 8 4 7 1 => C
3 1 3 4 2 12 & 5 3 8 4 7 1 => T
3 4 1 2 2 13 & 5 3 8 4 7 1 => F
8 4 2 8 1 16 & 5 3 8 4 7 1 => {
```

I am not going to take credit for the solution, but my teammate GoldenBushRobin identified that the dot product of the two vectors corresponds to the necessary ASCII value. 

```python
import numpy as np
with open("output.txt", "r") as file:
    for line in file:
        b = [5, 3, 8, 4, 7, 1]
        line = line.strip()
        line = line.split(" ")
        # convert to int
        line = [int(x) for x in line]
        product = np.dot(line, b)
        print(chr(product), end="")

# PCTF{M0r3!_C0mpET1tIve_CyB3R_@_M4$$on}
```

The flag is `PCTF{M0r3!_C0mpET1tIve_CyB3R_@_M4$$on}`.




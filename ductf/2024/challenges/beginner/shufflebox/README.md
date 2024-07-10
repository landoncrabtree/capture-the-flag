# shufflebox

## Description

I've learned that if you shuffle your text, it's elrlay hrda to tlle htaw eht nioiglra nutpi aws.

Find the text censored with question marks in `output_censored.txt` and surround it with `DUCTF{}`.

Author: hashkitten


## Files

* [shufflebox.py](files/shufflebox.py)

* [output_censored.txt](files/output_censored.txt)

## Solution

The script `shufflebox.py` generates a permutation, `PERM` of the integers 0-16. Then, it uses `random.shuffle(PERM)` to shuffle the permutation. Lastly, it iterates through each line in an input file, grabbing the character at the index specified by the shuffled permutation, and writing it to an output file.

A simplified scenario:

```python
PERM = [0, 1, 2]
random.shuffle(PERM) -> [2, 0, 1]

input = "abc"
output = ""

for c in range(len(input)):
    output += input[PERM[c]]

print(output) -> "cab"
```

We are given the following output:

```
aaaabbbbccccdddd -> ccaccdabdbdbbada
abcdabcdabcdabcd -> bcaadbdcdbcdacab
???????????????? -> owuwspdgrtejiiud
```

We are given 2/3 of the shuffled output, and need to find the third, which is the flag.




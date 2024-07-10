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

We are given 2/3 of the shuffled output, and need to find the third, which is the flag. The first input we were given is grouped into four. Because the order of this, we can identify possible permutations for each group of four. For example, take `aaaa`. In the output, the index of the first `a` could be [2, 6, 13, or 15]. We can generate all possible permutations for each group of four, and then check the second input to find the correct permutation. Once we have the correct permutation, we can use it to find the flag.

A: 2, 6, 13, 15
B: 7, 9, 11, 12
C: 0, 1, 3, 4
D: 5, 8, 10, 14

These are the possible permutations for the first input. We can then check the second input to find the correct permutation. So, let's start with A:

permutation[0]:
- 2: `in2[0] == out2[2]` -> `a == a` Correct!
- 6: `in2[0] == out2[6]` -> `a == d` Incorrect
- 13: `in2[0] == out2[13]` -> `a == c` Incorrect
- 15: `in2[0] == out2[15]` -> `a == b` Incorrect

permutation[1]:
- 6: `in2[1] == out2[6]` -> `b == d` Incorrect
- 13: `in2[1] == out2[13]` -> `b == c` Incorrect
- 15: `in2[1] == out2[15]` -> `b == b` Correct!

permutation[2]:
- 6: `in2[2] == out2[6]` -> `c == d` Incorrect
- 13: `in2[2] == out2[13]` -> `c == c` Correct!

permutation[3]:
- 6: `in2[3] == out2[6]` -> `d == d` Correct!

So, the first four of the permutation is `[2, 15, 13, 6]`. We continue this process for the other three groups of four, and then use the correct permutation to find the flag. We can automate this entire process with the following script:

```python
def solve():
    in1 = 'aaaabbbbccccdddd'
    out1 = 'ccaccdabdbdbbada'
    in2 = 'abcdabcdabcdabcd'
    out2 = 'bcaadbdcdbcdacab'
    
    perms = []
    
    # Break in1 into chunks of four
    # We know it was shuffled in order, so we can generate possible permutations
    # ie: The first four A's have to be mapped to [2, 6, 13, 15], B's to ...
    in1_groups = in1[0:4], in1[4:8], in1[8:12], in1[12:16]
    
    # Find each possible permutation index
    for group in in1_groups:
        for i in range(4):
            perms.append(out1.index(group[i]))
            out1 = out1.replace(group[i], '_', 1)
     
    print(perms)
    # Now we have a list of possible permutations, can break into chunks of four and validate against in2
    perms = [perms[i:i+4] for i in range(0, len(perms), 4)]
    in2_groups = in2[0:4], in2[4:8], in2[8:12], in2[12:16]
    
    final_perm = []
    
    # Check each group of four in in2 against the possible permutations to find the correct one
    for i, group in enumerate(in2_groups):
        for j in range(4):
            for p in perms[i]:
                if out2[p] == group[j]:
                    final_perm.append(p)
    
    print(final_perm)
    
    # ???????????????? -> owuwspdgrtejiiud
    
    print(''.join(['owuwspdgrtejiiud'[p] for p in final_perm]))

perm = solve()
```




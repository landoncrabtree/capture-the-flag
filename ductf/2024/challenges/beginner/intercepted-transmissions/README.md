# Intercepted Transmissions

## Description

Those monsters! They've kidnapped the Quokkas! Who in their right mind would capture those friendly little guys.. We've managed to intercept a CCIR476 transmission from the kidnappers, we think it contains the location of our friends! Can you help us decode it? We managed to decode the first two characters as '##'

NOTE: Wrap the decoded message in `DUCTF{}`.

Author: Pix


## Files

* [encoding](files/encoding)


## Solution

We're told that the transmission is CCIR476 encoded. A quick [search](https://en.wikipedia.org/wiki/CCIR_476) tells us that it is a radio communication protocol where each character is represented by a 7-bit code. Four of the bits are `1` and three are `0`, to allow for single bit error correction.

All we need is a mapping of the 7-bit code to the character it represents, which we can find [here](https://web.archive.org/web/20220211215211/http://www.discolodxgroup.cl/documentos/otros/ARRL%202013%20Handbook/ARRL%202013%20Handbook%20Supplemental%20Files/Chapter%2016/ITA2-CODES.pdf).

There are two special control characters, `LTRS` and `FIGS`, which switch between letters and figures respectively, so we need to keep track of what mode we're in.

```python
binary = '101101001101101101001110100110110101110100110100101101101010110101110010110100101110100111001101100101101101101000111100011110011011010101011001011101101010010111011100100011110101010110110101011010111001011010110100101101101010110101101011001011010011101110001101100101110101101010110011011100001101101101101010101101101000111010110110010111010110101100101100110111101000101011101110001101101101001010111001011101110001010111001011100011011'


# 47 A — —
# 72 B ? ?
# 1D C : :
# 53 D 5 $
# 56 E 3 3
# 1B F 4 !
# 35 G 4 &
# 69 H 4 # or motor stop
# 4D I 8 8
# 17 J BELL ´
# 1E K ( (
# 65 L ) )
# 39 M . .
# 59 N , ,
# 71 0 9 9
# 2D P 0 0
# 2E Q 1 1
# 55 R 4 4
# 4B S ' BELL
# 74 T 5 5
# 4E U 7 7
# 3C V = ;
# 27 W 2 2
# 3A X / /
# 2B Y 6 6
# 63 Z + "
# 78 ← CR (Carriage return)
# 6C ≡ LF (Line feed)
# 5A ↓ LTRS (Letter shift)
# 36 ↑ FIGS (Figure shift)
# 5C SP (Space)
# 6A BLK (Blank)

LTRS = {
    '47': 'A',
    '72': 'B',
    '1D': 'C',
    '53': 'D',
    '56': 'E',
    '1B': 'F',
    '35': 'G',
    '69': 'H',
    '4D': 'I',
    '17': 'J',
    '1E': 'K',
    '65': 'L',
    '39': 'M',
    '59': 'N',
    '71': 'O',
    '2D': 'P',
    '2E': 'Q',
    '55': 'R',
    '4B': 'S',
    '74': 'T',
    '4E': 'U',
    '3C': 'V',
    '27': 'W',
    '3A': 'X',
    '2B': 'Y',
    '63': 'Z',
    '78': '\r',
    '6C': '\n',
    '5A': 'LTRS',
    '36': 'FIGS',
    '5C': ' ',
    '6A': '' # blank
}

FIGS = {
    '47': 'A',
    '72': '?',
    '1D': ':',
    '53': '$',
    '56': '3',
    '1B': '!',
    '35': '&',
    '69': '#',
    '4D': '8',
    '17': '´',
    '1E': '(',
    '65': ')',
    '39': '.',
    '59': ',',
    '71': '9',
    '2D': '0',
    '2E': '1',
    '55': '4',
    '4B': '\a', # BELL
    '74': '5',
    '4E': '7',
    '3C': ';',
    '27': '2',
    '3A': '/',
    '2B': '6',
    '63': '"',
    '78': '\r',
    '6C': '\n',
    '5A': 'LTRS',
    '36': 'FIGS',
    '5C': ' ',
    '6A': '' # blank
    
}

current = "LTRS"
flag = ""

# split into chunks of seven
chunks = [binary[i:i+7] for i in range(0, len(binary), 7)]
print(chunks)

for chunk in chunks:
    h = hex(int(chunk, 2))[2:].upper()
    if current == "LTRS":
        char = LTRS.get(h)
        if char == "FIGS":
            current = "FIGS"
        elif char == "LTRS":
            pass
        else:
            flag += char
    else:
        char = FIGS.get(h)
        if char == "FIGS":
            pass
        elif char == "LTRS":
            current = "LTRS"
        else:
            flag += char

print(flag)
```



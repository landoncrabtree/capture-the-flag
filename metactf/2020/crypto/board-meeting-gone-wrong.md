# Board Meeting Gone Wrong - 325pts
Tools: `Python, Hashcat, John The Ripper`
> I stole this sensitive document that contains some really important board notes. I have a feeling I can get some serious insight on stonks here. There are a few things I know about the person I stole it from. He likes animals, he likes to speak like he's a hacker to make himself seem cool, and he was born in 1972. I hope that helps. Can you help me crack it? I will make sure to share some of the profits.
<hr>

I began by finding a basic animal wordlist. I found [this](https://github.com/sroberts/wordlists/blob/master/animals.txt) and downloaded it.

```shell
wget https://github.com/sroberts/wordlists/blob/master/animals.txt
```

Then, I needed to convert the animals into leetspeak. I created a Python script to do this.

```python
leet = {
    'a': '@',
    'e': '3',
    'i': '1',
    'o': '0',
    's': '5',
    't': '7'
}
out = open("out.txt", 'a')
with open("animals.txt") as f:
    for line in f:
        line.strip()
        replaced = ""
        for c in line:
            if c in leet:
                replaced += leet.get(c)
            elif c == '\n':
                replaced += "1972" + "\n"
            else:
                replaced += c
        out.write(replaced)
```
This script opens `animals.txt` and replaces characters based on their keypairs in the leet dictionary. It then appends 1972 to the end of the string and writes it to `out.txt`.

Now, we have our wordlist. We must prepare `Board_Meeting_Notes.docx` for cracking. First, we will use `office2john` to create a hash for the docx file. Running `office2john out.txt > hash` will give us our hash file. Then, we can use Hashcat to crack the hash. (You could also use John, but I decided to use Hashcat as I used John in the last password cracking challenge.)

```shell
$ hashcat -a 0 -m 9600 hash out.txt
>> $office$*2013*100000*256*16*e6e06de5805713d9d971f4bcb249e0c6*34a42cf8762b521292400e6854d4be75*a1a5a0a3b7038ab0fd37115744a0ca264e4f88a33110bed83440ca9668e9b138:d0lph1n1972
```

We can then use the cracked password to open the docx and obtain the flag.

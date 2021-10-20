**Python Wrangling** | Syreal

We are given three files:
`ende.py`
`pw.txt`
`flag.txt.en`

Running the Python script using `python3 ende.py`:
```
Usage: ende.py (-e/-d) [file]
```

I'm not sure what the arguments are, so let's try to run it with -h to see if there is a help message: `python3 ende.py -h`
```
Usage: ende.py (-e/-d) [file]
Examples:
  To decrypt a file named 'pole.txt', do: '$ python ende.py -d pole.txt'
```

That helps us out a lot.  So, we know we have to decrypt the `flag.txt.en` file, so let's run `python3 ende.py -d flag.txt.en`, and we will see:
```
Please enter the password:
```

We are already given the password, we just have to put it in. `cat pw.txt` shows us that the password is `dbd1bea4dbd1bea4dbd1bea4dbd1bea4` and using that as the password:
```
picoCTF{4p0110_1n_7h3_h0us3_dbd1bea4}
```

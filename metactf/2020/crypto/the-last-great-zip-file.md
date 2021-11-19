# The Last Great Zip File - 200pts
Help! I've created a zip archive that contains my favorite flag, but I forgot the password to it. Can you help me recover my flag back?

You may need to use another program such as wget to download the file if your browser is blocking the download. Now to get the password hash from the zip file...
<hr>

We can use zip2john to convert the encrypted zip file to a format that can be cracked by John. 

```shell
zip2john flag.zip > hash
```

Then, we can use John alongside rockyou.txt to crack the password.

```shell
john --format=PKZIP --wordlist=/usr/share/wordlists/rockyou.txt hash
```

This will reveal the zip password to be "Soldat*13" which allows us to open the zip and reveal the flag.


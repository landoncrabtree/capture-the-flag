# Solution

For this challenge, we are given `corrupted.jpg`. Trying to open the image leads to an error. I first ran `file corrupted.jpg` to determine if maybe the header bytes were wrong-- this is a common CTF problem, however, the image was indeed a JPEG. I then ran `xxd corrupted.jpg` to see if there was any weird data in the actual bytes of the image, and saw this:

![hexdump](https://i.imgur.com/fhOD8gZ.png)

If we look carefully, we will see things like CORRUPTED**g**CORRUPTED**r**CORRUPTED**K** and so on. It looks like they've added "CORRUPTED" in between bytes, so we can write a Python script to remove these and recover the image.

```python
with open("corrupted.jpg", "rb") as f:
    data = f.read()
    data = data.replace(b"CORRUPTED", b"")
    with open("fixed.jpg", "wb") as f2:
        f2.write(data)
```

Now we have recovered a working image, but it doesn't look like there's anything special. Running `strings fixed.jpg` to try and see if the flag was there reveals `Monitor.jpgPK` at the end of the file. `PK` is the magic bytes for a ZIP file, so we have a ZIP file hidden inside the image containing `Monitor.jpg`. We can extract it using binwalk:

```bash
binwalk -eM fixed.jpg
```

Now we have recovered `Monitor.jpg`, which states "Not a Flag". I performed some basic stego (exiftool, strings, binwalk), but didn't find anything. My typical next step for stego is [aperisolve](https://www.aperisolve.com/) as you can upload an image and it will run a lot of stego tools for you. After uploading the image, and looking at the superimposed version

![superimposed](https://i.imgur.com/H76Hjah.png)

we notice what looks like a flag on the bottom of the monitor. All we need to do is open the image and increase the exposure or brightness to see the flag:

`PCTF{00ps_1_L1ed_Th3r3_1s_4_Fl4g}`



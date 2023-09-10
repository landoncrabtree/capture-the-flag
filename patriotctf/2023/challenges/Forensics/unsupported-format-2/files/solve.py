with open("corrupted.jpg", "rb") as f:
    data = f.read()
    data = data.replace(b"CORRUPTED", b"")
    with open("fixed.jpg", "wb") as f2:
        f2.write(data)
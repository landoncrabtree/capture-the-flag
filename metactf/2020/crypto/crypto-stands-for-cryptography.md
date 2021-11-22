# Crypto Stands for Cryptography - 100 pts
> Welcome to the crypto team! We help consult in a variety of areas around the security department, helping to make sure our company is using proper encryption, data storage, and data transfer mechanisms. The data security team said they currently use something called Base64 to "encrypt" data. They want to know if that's a secure way to store sensitive data, and provided a sample of data: TWV0YUNURntiYXNlNjRfZW5jMGRpbmdfaXNfbjB0X3RoZV9zYW1lX2FzX2VuY3J5cHRpMG4hfQ== Is it secure? Can you crack it?
<hr>

The flag for this challenge can be found by decoding the base64 string.
```shell
echo "TWV0YUNURntiYXNlNjRfZW5jMGRpbmdfaXNfbjB0X3RoZV9zYW1lX2FzX2VuY3J5cHRpMG4hfQ==" | base64 --decode
```


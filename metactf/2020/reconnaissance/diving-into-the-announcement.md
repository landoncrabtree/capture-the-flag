# Diving Into the Announcement - 225pts
> Vulnerabilities are patched in software all the time, and for the most serious ones, researchers work to build proof-of-concept (POC) exploits for them. As defenders, we need to continuously monitor when new public exploits drop, figure out how they work, and ensure we're protected against them. Recently, Microsoft announced CVE-2020-1472. Your task is to locate a public exploit for it and identify the vulnerable function that the POCs call. The flag will be the function's name.
<hr>

CVE-2020-1472 ("Zerologon"): "An elevation of privilege vulnerability exists when an attacker establishes a vulnerable Netlogon secure channel connection to a domain controller"

VoidSec has a published checker and exploit code [here](https://github.com/VoidSec/CVE-2020-1472). Taking a look at their `cve-2020-1472-exploit.py`, we will find their attempt to authenticate using the vulnerability:

```python
    try:
        server_auth = nrpc.hNetrServerAuthenticate3(
            rpc_con, dc_handle + "\x00", target_computer + "$\x00",
            nrpc.NETLOGON_SECURE_CHANNEL_TYPE.ServerSecureChannel,
                     target_computer + "\x00", ciphertext, flags
        )
 ```
 
 Thus, the vulnerable function (and our flag) is `hNetrServerAuthenticate3`.

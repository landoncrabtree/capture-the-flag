# Staging in 1... 2... 3 - 150pts
> The Incident Response (IR) team identified evidence that a Threat Actor accessed a system that contains sensitive company information. The Chief Information Security Officer (CISO) wants to know if any data was accessed or taken. There was a suspicious file created during the timeframe of Threat Actor activity: C:\123.tmp. Can you check it out?
<hr>

To find the flag, the file can be analyzed using
```shell
strings 123.tmp
```

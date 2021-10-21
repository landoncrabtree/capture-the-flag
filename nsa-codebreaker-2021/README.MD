# Overview
 The 2021 Codebreaker Challenge consists of a series of tasks that are worth a varying amount of points based upon their difficulty. Schools will be ranked according to the total number of points accumulated by their students. Solutions may be submitted at any time for the duration of the Challenge.

While not required, we recommend that you solve tasks in order, since they flow with the storyline. Later tasks may rely on artifacts / inputs from earlier tasks.

Each task in this year's challenge will require a range of skills. We need you to call upon all of your technical expertise, your intuition, and your common sense. 


## Task 1:
The NSA Cybersecurity Collaboration Center has a mission to prevent and eradicate threats to the US Defense Industrial Base (DIB). Based on information sharing agreements with several DIB companies, we need to determine if any of those companies are communicating with the actor's infrastructure.

You have been provided a capture of data en route to the listening post as well as a list of DIB company IP ranges. Identify any IPs associated with the DIB that have communicated with the LP. 

Files:
* `capture.pcap`
* `ip_ranges.txt`

First, I opened `capture.pcap` using Wireshark. Then, it was a simple filter to see which IP(s) had interactions. Using the filter `ip.addr == XX.XX.XX.XX/XX` for each CIDR notation will show which IP addresses interacted with the LP. 

![Wireshark](https://i.imgur.com/MsIdGPz.png)

## Task 2:
NSA notified FBI, which notified the potentially-compromised DIB Companies. The companies reported the compromise to the Defense Cyber Crime Center (DC3). One of them, Online Operations and Production Services (OOPS) requested FBI assistance. At the request of the FBI, we've agreed to partner with them in order to continue the investigation and understand the compromise.

OOPS is a cloud containerization provider that acts as a one-stop shop for hosting and launching all sorts of containers -- rkt, Docker, Hyper-V, and more. They have provided us with logs from their network proxy and domain controller that coincide with the time that their traffic to the cyber actor's listening post was captured.

Identify the logon ID of the user session that communicated with the malicious LP (i.e.: on the machine that sent the beacon *and* active at the time the beacon was sent). 

Files:
* `oops_subnet.txt`
* `proxy.log`
* `logins.json`

To be honest, this task was a bit painstaking for me. I'm sure there was an easier way to achieve the goal, but for me, it was more trial and error and going one-by-one until I found the right result. First, I opened `proxy.log` to find which IP address was interacting with the LP. From Task 1, we know the LP to be `10.180.170.84` because that is the IP address that all IP ranges from Task 1 interacted with. So, we can simply search for `10.180.170.84` in `proxy.log`, and we  will see:

```
2021-03-16 08:36:11 38 172.28.245.238 200 TCP_MISS 12734 479 GET http tcthy.invalid chairman - - DIRECT 10.180.170.84 application/octet-stream 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36' PROXIED none - 172.28.245.54 SG-HTTP-Service - none -
```

The first thing that came to my mind was to look for '172.28.245.238', however, that yielded 108 results, and I did not feel like sifting for hours through JSON data. If we take a look at the `logins.json` file, we will notice timestamps are as follows: `"TimeCreated": "2021-03-16T12:20:44.9171085+00:00",`. So, I started by looking for the string '2021-03-16T08' in the logins file, to see if any users were active at the time. However, there were no results. This had me a bit stumped, so then I assumed it could be 24H time; therefore, T20, rather than T08. This provided results, but none using the '172.28.245.238' remote address. So, I then compared `logins.json` to `proxy.log`, and noticed that the timestamps are different. The first result in `proxy.log` is at 06:45:45 and in `logins.json` at 10:42:49. So there is a ~4 hour difference. I then looped back to `capture.pcap` and filtered by `http.request.method == "GET"` to find the GET request to 'tcthy.invalid', which shows an Epoch timestamp of '1615897943.847900000', or '2021-03-16T12:36:11'. 

So, now I had the proper timestamp to be looking for. We know the remote address has to be `172.28.245.238` and the user had to be active at `2021-03-16T12:36:11`. 

This took a bit of sifting through data and timestamps, but I was able to find:
```json
{"PayloadData1": "Target: OOPS\\reinoso.barbara", "PayloadData2": "LogonType 3", "PayloadData3": "LogonId: 0X386CF8", "MapDescription": "An account was logged off", "ChunkNumber": 0, "Computer": "OOPS-DC.oops.net", "Payload": "{\"EventData\": {\"Data\": [{\"@Name\": \"TargetUserSid\", \"#text\": \"S-1-5-21-8182753-126455048-1978990350-1100\"}, {\"@Name\": \"TargetUserName\", \"#text\": \"reinoso.barbara\"}, {\"@Name\": \"TargetDomainName\", \"#text\": \"OOPS\"}, {\"@Name\": \"TargetLogonId\", \"#text\": \"0X386CF8\"}, {\"@Name\": \"LogonType\", \"#text\": \"3\"}]}}", "Channel": "Security", "Provider": "Microsoft-Windows-Security-Auditing", "EventId": 4634, "EventRecordId": "6428", "ProcessId": 693, "ThreadId": 7836, "Level": "LogAlways", "Keywords": "Audit success", "SourceFile": "C:\\Windows\\system32\\winevt\\Logs\\Security.evtx", "ExtraDataOffset": 0, "HiddenRecord": false, "TimeCreated": "2021-03-16T14:24:38.0887578+00:00", "RecordNumber": "6428"}
```
The user `reinoso.barbara` with LogonID of `0X386CF8` was active on the remote address `172.28.245.238` (The IP address that made the request to the LP) up until 14:24:38, which was after the request was made. 

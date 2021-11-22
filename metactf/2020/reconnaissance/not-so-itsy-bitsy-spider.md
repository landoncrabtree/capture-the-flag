# Not So Itsy Bitsy Spider - 200pts
> Recent reporting indicates that a prominent ransomware operator, known as WIZARD SPIDER, was able to deploy Ryuk ransomware in an environment within 5 hours of compromise. What recent, critical vulnerability was exploited in this environment to gain elevated privileges? The flag will be in the following format: CVE-XXXX-XXXX
<hr>

I began looking for the answer by searching "Ryuk ransomware CVE 2021" and found CVE-2021-40444, which attacks Microsoft Office. However, that flag was incorrect. I then realized the challenge is from 2020, not 2021, so "latest" would refer to 2020 CVE's.  If we Google "Ryuk ransomware CVE" we can find a list of all known exploits that were used to infect systems with Ryuk (https://cybersecurity.bd.com/bulletins-and-patches/ryuk-ransomware) and we will find the most "recent" CVE.

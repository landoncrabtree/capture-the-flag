# [REDACTED] - 225pts
Tools: `Photoshop`
> The CEO of Cyber Corp has strangely disappeared over the weekend. After looking more into his disappearance Local Police Department thinks he might have gotten caught up into some illicit activities. The IT Department just conducted a search through his company-provided laptop and found an old memo containing a One Time Password to log into his e-mail. However it seems as if someone has redacted the code, can you recover it for us?
<hr>

For this challenge, I used Adobe Photoshop. I'm not sure if there's a similar method using other alternatives such as Gimp or Affinity, but I would assume there *should be*.


First, I opened `cybercorp_memo.pdf` using Photoshop. Then, an 'Import PDF' dialog box opened, allowing me to configure the way the PDF was imported. On the 'Select' option, rather than choosing 'Pages', I chose 'Images.' This will allow you to extract the layer below the black box.

![Photoshop Import PDF](https://i.imgur.com/O3gqJ3B.png)

Once you load the PDF that way, the flag will be revealed.

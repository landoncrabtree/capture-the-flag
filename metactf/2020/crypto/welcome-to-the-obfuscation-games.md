# Welcome to the Obfuscation Games - 175pts

During a recent incident response investigation, we came across this suspicious command executed by an attacker, and we'd like you to analyze it. Malware authors like to obfuscate their payloads to make it harder, but we're sure you're up to the task. See if you can figure out what's happening without even running it!

$s=New-Object IO.MemoryStream(,[Convert]::FromBase64String("H4sIAEFgjl8A/xXMMQrCQBCF4as8FltPIFaCnV3A8jFmn8ngupuYaUS8e5LyL77//vHQcWxLIHWj8Cw2wBd4RWyp2resjMm+pVlOJxzmGWekm8Iu3fU3ScXrwIf1L26C+4CtijukBY3hb/3TCj2Ieh9qAAAA"));IEX (New-Object IO.StreamReader(New-Object IO.Compression.GzipStream($s,[IO.Compression.CompressionMode]::Decompress))).ReadToEnd();
<hr>
Looking at the PowerShell script, we notice it takes a base64 string as a MemoryStream, and then creates a Gzip file using the memory stream. It then attempts to execute the decompressed gzip file using 'iex()'. Running the PowerShell code reveals that the flag is in the payload. We can simply pipe the decoded base64 string into a `gz` file, and then `gunzip` the file.

`echo "H4sIAEFgjl8A/xXMMQrCQBCF4as8FltPIFaCnV3A8jFmn8ngupuYaUS8e5LyL77//vHQcWxLIHWj8Cw2wBd4RWyp2resjMm+pVlOJxzmGWekm8Iu3fU3ScXrwIf1L26C+4CtijukBY3hb/3TCj2Ieh9qAAAA" | base64 --decode > meta.gz`.

Then, we can `gunzip meta.gz` to decompress the file, and use `cat meta` to view the file contents, revealing the flag.

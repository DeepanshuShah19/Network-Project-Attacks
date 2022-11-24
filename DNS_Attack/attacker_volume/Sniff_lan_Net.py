#!/usr/bin/env python3
''' PYTHON PROGRAM TO IMPLEMENTING IP SNIFFING USING SCAPY AND SOCKET PACKAGE'''

# import all the required libraries
import sys as _sys
import os as _os
import time as _time
from scapy.all import *
import socket as _socket
from struct import Struct as _Struct
from ipaddress import IPv4Address as _IPv4Address


# declare global variables to be used for the extract class

# convert and unpack tcp and udp header in redable form using struct
Unpack_tcp_header = _Struct('!2H2LB').unpack_from                                   
Unpack_udp_header = _Struct('!4H').unpack_from  

# write the error to stdout if found                           
_write_err = _sys.stdout.write
_fast_time = _time.time

# count occurence of errors
Count=0

# main class to UNPACK the packets & EXTRACT the details of the host 
class Extract:

    # init function to initialize the object's attributes to the class
    def __init__(self, data):                                                       
        self._name = self.__class__.__name__                                    
        # variable for destination MAC address
        self.Destination_MAC = data[:6].hex()                                      
        self.timestamp = _fast_time()
        # variable for source MAC address
        self.Source_MAC = data[6:12].hex()                                          
        # variable to store protocol number
        self.Protocol  = 0                                                          
        self._data   = data[14:]
        self._dlen = len(data)

    # str method to represent class objects as strings and display the sniffed data
    def __str__(self):                                                             
        return '\n'.join([
            f'{"="*32}',
            f'{" "*8} Packet Sniffed from the Networks',
            f'{"="*32}',
            f'{" "*8}ETHERNET',
            f'{"-"*32}',
            f' SOURCE MAC Address: {self.Source_MAC}',
            f' DESTINATION MAC Address: {self.Destination_MAC}',
            f'{"-"*32}',
            f'{" "*8}IP',
            f'{"-"*32}',
            f'Header-Length: {self.Header_length}',
            f'Protocol: {self.Protocol}',
            f'SOURCE-IP: {self.Source_IP}',
            f'DESTINATION-IP: {self.Destination_IP}',
            f'{"-"*32}',
            f'{" "*8}UTILISED PORT',
            f'{"-"*32}',
            f'SOURCE-port: {self.Source_Port}',
            f'DESTINATION-port: {self.Destination_Port}',
            f'{"-"*32}',
            f'{" "*8}DATA',
            f'{"-"*32}',
            f'{self.Payload}'
        ])

    # utility function to slice IP data
    def _IP(self):
        data = self._data
        # extract source IP address from IPV4Address library
        self.Source_IP = _IPv4Address(data[12:16])
        # extract destination IP address from IPV4Address library                                      
        self.Destination_IP = _IPv4Address(data[16:20])                                      
        # extract header length from IPV4Address library
        self.Header_length = (data[0] & 15) * 4
        # extract protocol information from IPV4Address library
        self.Protocol  = data[9]
        # extract IP header length from IPV4Address library
        self.ip_header = data[:self.Header_length]
        # extract IP header from payload using IPV4Address library
        self._data = data[self.Header_length:]                                          

    # utility function to slice tcp header information
    def _TCP(self):
        data = self._data
        # object to unpack tcp details
        TCP_header = Unpack_tcp_header(data)
        # extract tcp source port number from tcp header
        self.Source_Port = TCP_header[0]
        # extract tcp destination port number from tcp header
        self.Destination_Port = TCP_header[1]
        # extract tcp sequence number from tcp header
        self.sequence_number = TCP_header[2]
        # extract tcp ack number from tcp header
        self.acknowledgement_number = TCP_header[3]
        # extract tcp header length 
        Header_length = (TCP_header[4] >> 4 & 15) * 4
        # header length slicing
        self.proto_header = data[:Header_length]
        # extract tcp header from payload
        self.Payload = data[Header_length:]
    
    # utility function to slice udp header information
    def _UDP(self):                                                                 
        data = self._data
        # object to unpack udp details
        UDP_header = Unpack_udp_header(data)
        # extract udp source port number from udp header
        self.Source_Port = UDP_header[0]
        # extract udp destination port number from udp header
        self.Destination_Port = UDP_header[1]
        # extract udp length from udp header
        self.udp_length  = UDP_header[2]
        # extract udp checksum from udp header
        self.udp_check  = UDP_header[3]
        # extract udp header
        self.proto_header = data[:8]
        # extract udp header from payload
        self.Payload = data[8:]
    
    # utility function to unpack the tcp and udp packets
    def parse(self):
        # initialize object to access IP method
        self._IP()
        # identify TCP protocol number and call tcp method 
        if (self.Protocol == 6):
            self._TCP()
        # identify UDP protocol number and call udp method
        elif (self.Protocol == 17):
            self._UDP()
        # if protocol not found, print error message
        else:
            _write_err('TCP/UDP PACKETS not found!\n')

# function to initialize class and giving data to packets
def parse(data):
    try:
        # initialize class method
        Packet = Extract(data)
        # call parse function with the packets
        Packet.parse()                        
        print(Packet)
    except:
        # if error, pass
        pass

# function to get the lAN information
def Inside_Lan(pckt, Count=0):
    # filter the LAN Ip and print the source, destination IP and protocol
    if "5.5.0" in pckt[IP].src and "5.5.0" in pckt[IP].dst:
        print(" Source IP of the LAN ->", pckt[IP].src)
        print(" Destination IP of the LAN ->", pckt[IP].dst)
        print(" LAN Protocol ->", pckt[IP].proto)
        print("\n")

# driver code to run the program
if __name__ == '__main__':
    if _os.geteuid():
        _sys.exit('Run the file from the ROOT!')
    print("Started SNIFFING packets from LAN...")
    interface_id = str(subprocess.check_output("ip a | grep 5.5.0", shell=True)).split(" ")[-1][:-3]
    pkt = sniff(iface=interface_id, filter='ip',prn=Inside_Lan)                  
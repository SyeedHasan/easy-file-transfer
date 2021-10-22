import socket
import tqdm
import os

# IPv4 to bind the connection to
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 60034

# Buffer
BUFFER_SIZE = 4096

# Separator, if any
SEPARATOR = ","

# TCP Socket
s = socket.socket()

# Local IP Bind
s.bind((SERVER_HOST, SERVER_PORT))

# Accepting 15 new connections
s.listen(15)

print(f"[*] Listening at {SERVER_HOST}:{SERVER_PORT}")

i=1

while True:
	sc, address = s.accept()

	f = open('file_'+ str(i)+".pdf",'wb')
	i=i+1
	while (True):       
		l = sc.recv(1024)
		while (l):
				f.write(l)
				l = sc.recv(1024)

		break
	print("File closed.")
	f.close()
	sc.close()

s.close()

def receiveFiles():
	client_socket, address = s.accept()
	# if below code is executed, that means the sender is connected
	print(f"[+] {address} is connected.")

		# receive the file infos
		# receive using client socket, not server socket
	#while client_socket:
	try:
		while True:
			received = client_socket.recv(BUFFER_SIZE).decode()
			filename, filesize = received.split(SEPARATOR)
			# remove absolute path if there is
			filename = os.path.basename(filename)
			# convert to integer
			filesize = int(filesize)
			totalBytes = 0
			# start receiving the file from the socket
			# and writing to the file stream
			progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
			with open(filename, "wb") as f:
				while True:
					# read 1024 bytes from the socket (receive)
					bytes_read = client_socket.recv(BUFFER_SIZE)
					if not bytes_read:
					# nothing is received
					# file transmitting is done
						break

					totalBytes += bytes_read
					if totalBytes < filesize:
						# write to the file the bytes we just received
						f.write(bytes_read)
						# update the progress bar
						progress.update(len(bytes_read))

					if totalBytes == filesize:			
						progress.update(len(bytes_read))
						break


	#		client_socket.close()
	#		s.close()
	except Exception as e:
		print(e)
		pass

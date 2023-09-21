import socket

BYTES_TO_READ = 4096

def get(host, port):
    request = b"GET / HTTP/1.1\nHost: " + host.encode('utf-8') + b"\n\n"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # initialize a socket
        s.connect((host, port)) # connect to google
        s.send(request) # request google homepage
        s.shutdown(socket.SHUT_WR) # done sending request
        result = s.recv(BYTES_TO_READ) # receiving the response
        while(len(result) > 0):
            print(result)
            result = s.recv(BYTES_TO_READ)

# get("www.google.com", 80)
get("localhost", 8080)
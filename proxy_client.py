import socket

BYTES_TO_READ = 4096

def get(host, port):
    request = b"GET / HTTP/1.1\nHost: www.google.com\n\n"
    # AF_INET => IPV4, SOCK_STREAM => TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
        s.connect((host, port)) 
        s.send(request) 
        s.shutdown(socket.SHUT_WR) 
        chunk = s.recv(BYTES_TO_READ) 
        result = b'' + chunk

        while(len(result) > 0):
            chunk = s.recv(BYTES_TO_READ)
            result = chunk
        s.close()
        return result

get("localhost", 8080)
import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

# send some data(request) to host:port
def send_request(host, port, request):
    # create a new socket in with block to ensure it's closed once done
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # connect the socket to host:port
        client_socket.connect((host, port)) 
        # send the request through the connected socket
        client_socket.send(request) 
        # shut the socket to further writes. tells server done sending
        client_socket.shutdown(socket.SHUT_WR) 
        # assemble response
        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data
        while len(data) > 0: # continue reading data until connection terminates
            data = client_socket.recv(BYTES_TO_READ)
            result += data
        return result

# handle an incoming connection that has been accepted by the server
def handle_connection(conn, addr):
    with conn:
        print(f'Connected by {addr}')

        request = b''
        while True: # while socket open
            data = conn.recv(BYTES_TO_READ) # read data from socket
            if not data: # closed socket
                break
            print(data)
            request += data
        response = send_request("www.google.com", 80, request) # request to www.google.com
        conn.sendall(response) # return the response from www.google.com back to client

# start single-threaded proxy server
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # bind the server to a specific host and port on this machine
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))

        # allows us to reuse this socket address during linger
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)
    
        # wait for connection, accept it and create new socket called 'conn' to interact with it
        conn, addr = server_socket.accept()
    
        # pass 'conn' off to handle_connection to do some logic
        handle_connection(conn, addr)
        

# start multi-threaded proxy server
def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)
        
        while True:
            conn, addr = server_socket.accept()
            thread = Thread(target=handle_connection, args=(conn, addr)) 
            thread.run()

start_server()
# start_threaded_server()
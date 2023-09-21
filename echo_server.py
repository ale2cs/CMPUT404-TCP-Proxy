import socket
from threading import Thread

BYTES_TO_READ = 4096
HOST = "127.0.0.1" # ip, localhost
PORT = 8080

def handle_connection(conn, addr):
    with conn:
        print(f'Connected by {addr}')
        while True:
            data = conn.recv(BYTES_TO_READ) # wait for a request
            if not data: #receive empty byte string
                break
            print(data)
            conn.sendall(data)

# start single threaded echo server
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))

        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)
    
        conn, addr = server_socket.accept()
    
        handle_connection(conn, addr)


# start mutlithreaded echo server
def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(2) # allow backlog of up to 2 connections in queue
        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()



# start_server()
start_threaded_server()
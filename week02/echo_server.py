import socket
import sys
from pathlib import *

HOST = "127.0.0.1"
PORT = 5000

def echo_server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)    
    except socket.error as se:
        print(se)
        sys.exit(1)

    print("wait connect...............")
    while True:
        path = Path(__file__)
        parent_path = path.resolve().parent
        file_path = parent_path.joinpath("test_r.jpg")
        conn, addr = s.accept()
        print(f"connected by {addr}")
        with open(file_path, 'wb') as fp:
            while True:
                data = conn.recv(1024)
                fp.write(data)
        conn.close()
    s.close()


if __name__ == "__main__":
    echo_server()




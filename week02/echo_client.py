import socket
import sys
from pathlib import *


HOST = "127.0.0.1"
PORT = 5000

def echo_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
    except socket.error as se:
        print(se)
        sys.exit(1)
    
    path = Path(__file__)
    parent_path = path.resolve().parent
    file_path = parent_path.joinpath("test.jpg")
    with open(file_path, "rb") as f:
        while True:
            data = f.read(1024)
            if not data:
                print(f"upload end ========> {file_path}")
                break
            s.send(data)
        s.close()
  


if __name__ == "__main__":
    echo_client()




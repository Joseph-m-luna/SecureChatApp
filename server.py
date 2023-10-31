import socket
import time

def runserver(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    con, addr = s.accept()
    with con:
        print("connected")
        data = con.recv(1024).decode()
        print(data)
        for i in range(30):
            msg = f"message {i} "
            con.send(msg.encode())
            time.sleep(1)
            

if __name__  == "__main__":
    runserver("127.0.0.1", 9001)
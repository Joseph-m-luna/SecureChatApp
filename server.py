import socket
import time
import json as pickle

class connection:
    def __init__(self, con, addr):
        self.con = con
        self.addr = addr

        self.keep_alive = True
    
    def decode_msg(self, data):
        #TODO: when encryption is implemented, decrypt data prior to unloading

        #deserialize data
        decoded_data = data.decode()
        print("decoded: ", decoded_data)
        message_dict = pickle.loads(data)
        print(message_dict)

        return message_dict
    
    def keep_listening(self):
        with self.con:
            print("connected")
            while self.keep_alive:
                data = self.con.recv(1024)
                data = self.decode_msg(data)

                print(data)

                #TODO: handle message rather than just printing it (aka send it to all other clients)
class server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def runserver(self):
        #create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))

        #listen for new connections TODO: implement 10+ threaded chat clients rather than just one.
        s.listen()
        con, addr = s.accept()
        
        #maintain list of connections (For now just one)
        cons = []
        cons.append(connection(con, addr))
        cons[-1].keep_listening() #TODO: add threading to this            

if __name__  == "__main__":
    serv = server("127.0.0.1", 9001)
    serv.runserver()
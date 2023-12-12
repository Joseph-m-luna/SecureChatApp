import socket
import threading
from datetime import datetime
import time
import json
import ssl

PRIV_KEY_PATH = "./crypto/private.key"
CERTIFICATE_PATH = "./crypto/certificate.pem"

class connection:
    def __init__(self, con, addr):
        self.con = con
        self.addr = addr
    
    def decode_msg(self, data):
        #deserialize data
        decoded_data = data.decode()
        print("decoded: ", decoded_data)
        message_dict = json.loads(data)

        return message_dict
    
   
class server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames =[]
        self.limit = 10

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def removeClient(self, client):
        #remove client from client list
        index = self.clients.index(client)
        self.clients.remove(client)
        client.close()
        nickname = self.nicknames[index]

        #inform uesrs of disconnection
        leave_msg = {"data": f"{nickname} left the chat!", "time": (str(datetime.now())), "sender": "Server"}
        self.broadcast(json.dumps(leave_msg).encode("utf-8"))
        self.nicknames.remove(nickname)
        

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
                print(message)

                if not message:
                    self.removeClient(client)
                    break
            except:
                self.removeClient(client)
                break
                

    def setup_client(self, client, address, context, s):
        client = context.wrap_socket(client, server_side=True)
        print(f'Connected with {str(address)}')

        #get nickname of client
        message = {"metadata": "nick"}
        client.send(json.dumps(message).encode("utf-8"))
        nickname = json.loads(client.recv(1024).decode("utf-8"))["metadata"]
        self.nicknames.append(nickname)
        self.clients.append(client)

        #inform uesrs of connection
        print(f'Nickname of the client is {nickname}!')
        join_msg = {"data": f"{nickname} joined the chat!", "time": (str(datetime.now())), "sender": "Server"}
        self.broadcast(json.dumps(join_msg).encode("utf-8"))

        thread = threading.Thread(target=self.handle, args=(client,))
        thread.daemon = True
        thread.start()      

    def runserver(self):
        #create ssl context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=CERTIFICATE_PATH, keyfile=PRIV_KEY_PATH)

        #create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen()
        print(f'Listening on {(self.host, self.port)}...')

        try:
            while True:
                if len(self.clients) < self.limit:
                    #start secure connection
                    client, address = s.accept()

                    #set up connection
                    self.setup_client(client, address, context, s)

                else:
                    #check to see if the # of clients exceeds 10
                    #if yes: reject
                    #if no: handle client in separate thread and return to main loop
                    while True:
                        client, address = s.accept()
                        if len(self.clients) >= self.limit:
                            #print(len(self.clients))
                            client.close()
                        else:
                            #setup connection
                            self.setup_client(client, address, context, s)
                            break 
        except KeyboardInterrupt:
            print("\nCaught keyboard interrupt, exiting")
        finally:
            s.close()




if __name__  == "__main__":
    serv = server("127.0.0.1", 8080)
    serv.runserver()
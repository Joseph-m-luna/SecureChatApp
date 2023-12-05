import socket
import threading
import time
import json as pickle
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
        message_dict = pickle.loads(data)
        print(message_dict)

        return message_dict
    
   
class server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames =[]

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                # decrypt message
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(f'{nickname} left the chat!'.encode('ascii'))
                self.nicknames.remove(nickname)
                break

    def runserver(self):
        #create ssl context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=CERTIFICATE_PATH, keyfile=PRIV_KEY_PATH)

        #create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen()
        print(f'Listening on {(self.host, self.port)}...')

        while True:
            client, address = s.accept()
            client = context.wrap_socket(client, server_side=True)
            print(f'Connected with {str(address)}')

            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f'Nickname of the client is {nickname}!')
            self.broadcast(f'{nickname} joined the chat!'.encode('ascii'))
            client.send('\nConnected to the server!'.encode('ascii'))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.daemon = True
            thread.start()          

if __name__  == "__main__":
    serv = server("127.0.0.1", 9001)
    serv.runserver()
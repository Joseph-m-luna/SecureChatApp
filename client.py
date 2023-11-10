from tkinter import *
from datetime import datetime
import json as pickle
import time
import socket
import threading
import ssl

CERTIFICATE_PATH = "./crypto/certificate.pem"

################################
# GENERAL USE CASE:
#  * Input destination IP
#  * Input passcode
#  * If authenticated, client connects to the server
#  * Shake hands with the server and encrypt connection 
#  * (optional) load previous messages sent in the chat (could set a limit of like 10 previous messages)
#  * when messages are sent from the server, load them into the GUI
#  * when client sends message to server, server will send that out to the other clients
###############################
class TCP:
    def __init__(self, host, port):
        pass

class GUI:
    def __init__(self):
        # Set colorings
        self.black = "#000000"
        self.dark_grey = "#333333"
        self.light_grey = "474747"
        self.aqua_blue = "#00FFFF"
        self.white = "#FFFFFF"

        # Create window
        self.root = Tk()
        self.root.title("The Securest Chat App")
        self.root.iconbitmap("./chaticon.ico")
        self.root.geometry("500x700")
        self.root.configure(background=self.dark_grey)

        #Widget
        #Login label
        self.login_label = Label(self.root,text="Log In", font=("Helvetica, 32"), bg=self.dark_grey, fg=self.aqua_blue)

        # Username Label and Entry
        self.user_label = Label(self.root, text="Username: ", font=("Helvetica, 18"), bg=self.dark_grey, fg=self.white)
        self.user_entry = Entry(self.root)

        # IP address Label and Entry
        self.address_label = Label(self.root, text="Chatroom IP: ", font=("Helvetica, 18"), bg=self.dark_grey, fg=self.white)
        self.address_entry = Entry(self.root, show="*")

        #start connection button
        self.start_button = Button(self.root, text="Connect", font="Helvetica, 24", command=self.start_thread)

        # Wdiget Placement
        # Login
        self.login_label.place(relx=.5, rely=.2,anchor= CENTER)
        
        # User Label and Entry
        self.user_label.place(relx=.3, rely=.3,anchor= CENTER)
        self.user_entry.place(relx=.6, rely=.3,anchor= CENTER)
        
        # IP address Label and Entry
        self.address_label.place(relx=.3, rely=.35,anchor= CENTER)
        self.address_entry.place(relx=.6, rely=.35,anchor= CENTER)
        
        # Connect Button
        self.start_button.place(relx=.5, rely=.45,anchor= CENTER)

        #create label to update
        self.data = "waiting..."
        self.label = Label(self.root, text=self.data)
        # self.label.pack(pady=30)
        self.counter = 0

    def run(self):
        self.root.mainloop()
    
    def send_message(self, msg_data):
        #create dictionary for message data
        tcp_message = dict()

        #add contents to message
        tcp_message["data"] = msg_data
        tcp_message["time"] = str(datetime.now())
        tcp_message["sender"] = self.username

        #serialize message with pickle
        msg_serial = pickle.dumps(tcp_message)

        self.sec_con.sendall(msg_serial.encode("utf-8"))

    def recv_message(self):
        pass

    def update_label(self):
        self.data.set(f"{self.counter}")
        self.counter += 1
    
    def start_thread(self):
        #TODO: Switch screen to the chat screen

        #start thread for TCP connection
        threading.Thread(target=self.accept_connection).start()
    
    def accept_connection(self):
        #get username TODO: Once username box is implemented, we should get text from it. For now we set a static value
        self.username = self.user_entry.get()
        self.IP = self.address_entry.get()

        # create ssl context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(CERTIFICATE_PATH)
        context.check_hostname = False

        #create socket
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sec_con = context.wrap_socket(self.con)

        #connect to the server
        self.sec_con.connect((self.IP, 9001))

        for x in range(10):
            time.sleep(1)
            self.send_message(f"hello {x}")


    def connect(self, host, port):
        #definte connection information
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        for i in range(10):
            message = f"message {i}"
            s.sendall(message.encode("utf-8"))
            time.sleep(1)
        s.close()
    
if __name__ == "__main__":
    print()
    gui = GUI()
    gui.run()

from tkinter import *
from datetime import datetime
import json as pickle
import time
import socket
import threading

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
        # create window
        self.root = Tk()
        self.root.title("The Securest Chat App")
        self.root.iconbitmap("./chaticon.ico")
        self.root.geometry("500x800")

        #set colorings
        self.black="#000000"
        self.dark_grey = "#474747"
        self.light_grey = ""
        self.root.configure(background=self.dark_grey, )

        #start connection button
        self.start_button = Button(self.root, text="start tcp connection", font="Helvetica, 32", command=self.start_thread)
        self.start_button.pack(pady=100)

        #create label to update
        self.data = "waiting..."
        self.label = Label(self.root, text=self.data)
        self.label.pack(pady=30)
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

        self.con.sendall(msg_serial.encode("utf-8"))

    def recv_message(self):
        pass

    def update_label(self):
        self.data.set(f"{self.counter}")
        self.counter += 1
    
    def start_thread(self):
        threading.Thread(target=self.accept_connection).start()
    
    def accept_connection(self):
        #get username TODO: Once username box is implemented, we should get text from it. For now we set a static value
        self.username = "temp_name"

        #create socket
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #connect to the server
        self.con.connect(("127.0.0.1", 9001))

        #shake hands TODO: add encryption to connection when it is established here
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

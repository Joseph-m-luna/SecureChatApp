import tkinter as tk
from tkinter import *
from datetime import datetime
import json
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

# Set colorings
black = "#000000"
dark_grey = "#333333"
light_grey = "474747"
aqua_blue = "#00FFFF"
white = "#FFFFFF"

# Set Font
font_sm_bold=("Helvetica 12 bold")
font_sm=("Helvetica 12")
font_med=("Helvetica 18")
font_lrg=("Helvetica 32")

class TCP:
    def __init__(self, host, port):
        pass
 
class LoginScreen:
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
        
        self.nickname = ""
        
        # Widget Placement
        # self.msg.pack(pady=30)
        # self.msg.place(relx=.5, rely=.635,anchor= CENTER)
        # self.msg_entry.place(relx=.455, rely=.90,anchor= CENTER)
        # self.send_btn.place(relx=.855, rely=.90,anchor= CENTER)
        

        self.nickname = ""

    def on_closing(self):
        self.sec_con.close()
        self.root.quit()
        #self.root.destroy()

    def run(self):
        self.root.mainloop()
    
    def send_message(self):
        #get message text
        data = self.entry_field.get()

        if data:

            #create dictionary for message data
            tcp_message = dict()

            #add contents to message
            tcp_message["data"] = data
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
        #TODO: Switch screen to the chat screen

        #TODO: Create protections (if username is taken, inform user and don't connect. If IP is invalid, don't connect, inform user. Etc.)

        #create dummy message box for now
        self.make_chat_window()

        self.accept_connection()

        #start receive thread for TCP connection
        self.receive_thread = threading.Thread(target=self.recv_message, args=(self.sec_con,))
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def make_chat_window(self):
        self.root.title("Chat Application")

        # Create a frame for messages
        self.messages_frame = tk.Frame(self.root)
        self.messages_frame.pack(fill="both", expand=True)

        # Create a scrollbar for the message frame
        self.scrollbar = Scrollbar(self.messages_frame)
        self.scrollbar.pack(side="right", fill="y")

        # Create a label for each message
        self.messages = []

        # Create Entry widget for typing messages
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(side="bottom", fill="both", pady=5)
        self.entry_field = Entry(self.entry_frame)
        self.entry_field.pack(side="left", fill="both", expand=True)

        # Create Send button
        self.send_button = Button(self.entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(side="right")

        # Bind Enter key to send_message function
        self.entry_field.bind("<Return>", lambda event: self.send_message())
    
    def accept_connection(self):
        #get username TODO: Once username box is implemented, we should get text from it. For now we set a static value
        self.username = "temp_name"

        #create socket
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #secure socket
        self.sec_con = context.wrap_socket(self.con)

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
    gui = LoginScreen()
    gui.run()

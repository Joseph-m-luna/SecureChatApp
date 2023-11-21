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
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

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

            #serialize message with json
            msg_serial = json.dumps(tcp_message).encode("utf-8")

            self.sec_con.sendall(msg_serial)
            
            #remove text from input box
            self.entry_field.delete(0, "end")

    def recv_message(self, client):
        while True:
            try:
                data = client.recv(1024).decode("utf-8")
                data = json.loads(data)
                if len(data) == 1:
                    if data["metadata"] == "nick":
                        send_data = {"metadata": self.username}
                        client.send(json.dumps(send_data).encode("utf-8"))
                else:
                    if data["sender"] == self.username:
                        align = "w"
                    else:
                        align = "e"

                    #create message box
                    message_frame = tk.Frame(self.messages_frame, padx=10, pady=5, bd=2, relief=RAISED)
                    message_frame.pack(anchor=align, pady=5, padx=10, fill="both")

                    #create username label
                    username_label = Label(message_frame, text=data["sender"], font=("Helvetica", 10, "bold"))
                    username_label.pack(anchor=align)
                    
                    #create message label
                    message_label = Label(message_frame, text=data["data"], justify=LEFT)
                    message_label.pack(anchor=align)

                    #create metadata label
                    metadata_label = Label(message_frame, text=data["time"], font=("Helvetica", 8))
                    metadata_label.pack(anchor=align, pady=(5, 0))
            except Exception as error:
                print(f'An error occured {error}')
                client.close()
                break

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
        self.username = self.user_entry.get()
        self.IP = self.address_entry.get()

        #create ss1 context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(CERTIFICATE_PATH)
        context.check_hostname = False

        #create socket
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #secure socket
        self.sec_con = context.wrap_socket(self.con)

        #connect to the server
        try:
            self.sec_con.connect((self.IP, 9001))
        except:
            self.sec_con.close()
            self.root.quit()
    
if __name__ == "__main__":
    print()
    gui = GUI()
    gui.run()
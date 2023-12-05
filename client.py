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
       
        # Create window
        self.root = Tk()
        self.root.title("The Securest Chat App")
        self.root.iconbitmap("./chaticon.ico")
        self.root.geometry("500x700")
        self.root.configure(background=dark_grey)
        
        # Wdiget
        # Login Label
        self.login_label = Label(self.root,text="Log In", font=font_lrg, bg=dark_grey, fg=aqua_blue)
        # User Label and Entry
        self.user_label = Label(self.root, text="Username: ", font=font_med, bg=dark_grey, fg=white)
        self.user_entry = Entry(self.root)
        # IP Address Label and Entry
        self.address_label = Label(self.root, text="Chatroom IP: ", font=font_med, bg=dark_grey, fg=white)
        self.address_entry = Entry(self.root, show="*")
        # Start Connection Button
        self.start_button = Button(self.root, text="Connect", font=font_med, bg=aqua_blue, fg=black, command=self.connect)
    
        # Wdiget Placement
        # Login
        self.login_label.place(relx=.5, rely=.2,anchor= CENTER)
        # User Label and Entry
        self.user_label.place(relx=.3, rely=.3,anchor= CENTER)
        self.user_entry.place(relx=.6, rely=.3,anchor= CENTER)
        # IP Address Label and Entry
        self.address_label.place(relx=.3, rely=.35,anchor= CENTER)
        self.address_entry.place(relx=.6, rely=.35,anchor= CENTER)
        # Connect Button
        self.start_button.place(relx=.5, rely=.45,anchor= CENTER)
   
    def connect(self):
        self.username = self.user_entry.get()
        self.address = self.address_entry.get()

        # Close the login screen
        self.root.destroy()
        
        # Go to main screen
        main_screen = MainChatScreen(self.username, self.address)
        main_screen.run()
        
    def run(self):
        self.root.mainloop()
        
    def start_thread(self):
        pass
        
    
class MainChatScreen:
    def __init__(self, username, address):
       
        # Create window
        self.root = Tk()
        self.root.title("The Securest Chat App")
        self.root.iconbitmap("./chaticon.ico")
        self.root.geometry("500x700")
        self.root.configure(background=dark_grey)
        
        # Widget 
        # Username
        self.username = username
        self.username_label = Label(self.root, text="Username:" + self.username)
        self.username_label.pack(pady=20)
        # Password 
        self.address = address
        self.address_label = Label(self.root, text="Address: " + self.address)
        self.address_label.pack()
        # msg feed
        # msg input
        self.msg = Text(self.root, text="Message Feed", bg=aqua_blue, fg=black, font=font_sm, height=35)
        self.msg.pack(pady=(20,0))
        self.msg_entry = Entry(self.root, bg=white, fg=black, font=font_sm, width=50)
        self.msg_entry.pack(side=LEFT)
        # send msg btn
        # self.send_btn = Button(self.root, text="Send", font=font_sm_bold, bg=aqua_blue, fg=black, width=10, command=self.send_message)
 
        # side bar with chatroom name
        
        # Accept Connection
        self.accept_connection()
    
        #create label to update
        self.data = "waiting..."
        self.label = Label(self.root, text=self.data)
        self.label.pack(pady=40)
        self.counter = 0
        
        self.nickname = ""
        
        # Widget Placement
        # self.msg.pack(pady=30)
        # self.msg.place(relx=.5, rely=.635,anchor= CENTER)
        # self.msg_entry.place(relx=.455, rely=.90,anchor= CENTER)
        # self.send_btn.place(relx=.855, rely=.90,anchor= CENTER)
        

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
        
    def recv_message(self, client):
        while True:
            try:
                message = client.recv(1024).decode('ascii')
                if message == 'NICK':
                    client.send(self.nickname.encode('ascii'))
                else:
                    print(message)
            except:
                print('An error occured')
                client.close()
                break
            
    def write_message(self, client):
        message = 0
        while True:
            #TODO get input from user
            #message = f'{self.nickname}: {input("")}'
            time.sleep(5)
            
            #send_msg = self.send_message(str(message+1))
            send_msg = f"{self.username}: {str(message)}"
            client.send(send_msg.encode('ascii'))
            message += 1

    def update_label(self):
        self.data.set(f"{self.counter}")
        self.counter += 1
    
    def start_thread(self):
        threading.Thread(target=self.accept_connection).start()
    
    def accept_connection(self, address):
        self.port = 9001
        
        # Create ss1 context
        print("creating ss1")
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(CERTIFICATE_PATH)
        context.check_hostname = False
        
        # Create socket
        print("creating socket")
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Secure socket
        print("secure socket")
        self.sec_con = context.wrap_socket(self.con)
        
        # Connect to the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((address, self.port))
        for i in range(10):
            message = f"message {i}"
            s.sendall(message.encode("utf-8"))
            time.sleep(1)
        s.close()
        


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


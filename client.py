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
        self.login_label = Label(self.root,text="Log In", font=font_lrg, bg=dark_grey, fg=aqua_blue)
        self.user_label = Label(self.root, text="Username: ", font=font_med, bg=dark_grey, fg=white)
        self.user_entry = Entry(self.root)
        self.password_label = Label(self.root, text="Password: ", font=font_med, bg=dark_grey, fg=white)
        self.password_entry = Entry(self.root, show="*")
        self.start_button = Button(self.root, text="Connect", font=font_med, bg=aqua_blue, fg=black, command=self.connect)
    
        # Wdiget Placement
        self.login_label.place(relx=.5, rely=.2,anchor= CENTER)
        self.user_label.place(relx=.3, rely=.3,anchor= CENTER)
        self.user_entry.place(relx=.6, rely=.3,anchor= CENTER)
        self.password_label.place(relx=.3, rely=.35,anchor= CENTER)
        self.password_entry.place(relx=.6, rely=.35,anchor= CENTER)
        self.start_button.place(relx=.5, rely=.45,anchor= CENTER)
   
    def connect(self):
        username = self.user_entry.get()
        password = self.password_entry.get()
        
        # Check authenitciation here
        
        
        # Close the login screen
        self.root.destroy()
        
        # Go to main screen
        main_screen = MainChatScreen(username)
        main_screen.run()

    def run(self):
        self.root.mainloop()
        
    def start_thread(self):
        pass
        
    
class MainChatScreen:
    def __init__(self, username):
        # Create window
        self.root = Tk()
        self.root.title("The Securest Chat App")
        self.root.iconbitmap("./chaticon.ico")
        self.root.geometry("500x700")
        self.root.configure(background=dark_grey)
        
        # Widget 
        self.username = username
        self.username_label = Label(self.root, text=self.username)
        self.username_label.pack(pady=30)
        # msg feed
        # msg input
        self.msg = Text(self.root, bg=white, fg=black, font=font_sm, width=59)
        self.msg_entry = Entry(self.root, bg=white, fg=black, font=font_sm, width=52)
        # send msg btn
        self.send_btn = Button(self.root, text="Send", font=font_sm_bold, bg=aqua_blue, fg=black)
        # side bar with chatroom name
        
    
        #create label to update
        self.data = "waiting..."
        self.label = Label(self.root, text=self.data)
        self.label.pack(pady=40)
        self.counter = 0
        
        # Widget Placement
        self.msg.place(relx=.5, rely=.635,anchor= CENTER)
        self.msg_entry.place(relx=.455, rely=.90,anchor= CENTER)
        self.send_btn.place(relx=.855, rely=.90,anchor= CENTER)
        

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
    gui = LoginScreen()
    gui.run()
from tkinter import *
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

        #set custom title bar
        self.button = Button(self.root, text="close page", font="Helvetica, 32", command=self.root.quit)
        self.button.pack(pady=100)

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

    def update_label(self):
        self.data.set(f"{self.counter}")
        self.counter += 1
    
    def start_thread(self):
        threading.Thread(target=self.accept_connection).start()
    
    def accept_connection(self):
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.con.connect(("127.0.0.1", 9001))
        ready = "ready"
        self.con.sendall(ready.encode("utf-8"))
        while True:
            data = self.con.recv(1024).decode()
            self.label.config(text=data)

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
    gui = GUI()
    gui.run()

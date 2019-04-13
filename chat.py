from tkinter import *
from tkinter import messagebox
import threading
import socket


class Chat:
    def __init__(self, s, nickname):
        self.s = s
        self.HEIGHT = 640
        self.WIDTH = 640
        self.application_window = Tk()
        self.canvas = Canvas(self.application_window, height=self.HEIGHT, width=self.WIDTH)
        self.chat_frame = Frame(self.application_window, bg="gray")
        self.chat_text = Text(self.chat_frame, state="disabled")
        self.type_frame = Frame(self.application_window, bg="gray")
        self.contacts_frame = Frame (self.application_window, bg="gray")
        self.type_text = Text(self.type_frame)
        self.nickname = nickname
        self.type_message = ""
        self.data_type = "message"
        self.lb1 = Listbox(self.contacts_frame)
        print("Application initialized")

    def newsocket(self, s):
        self.s = s

    def receive(self):
            while True:
                data = self.s.recv(1024)
                self.chat_text.config(state="normal")
                self.chat_text.insert(INSERT, data)
                self.chat_text.config(state="disabled")

    def setnickname(self):
        pass

    def window(self):
        self.canvas.pack()
        self.application_window.title("Dzoiver")
        self.contacts_frame.place(relx=0.025, rely=0.025, relwidth=0.3, relheight=0.9)

        self.chat_frame.place(relx=0.33, rely=0.28, relwidth=0.63, relheight=0.45)

        self.type_frame.place(relx=0.33, rely=0.735, relwidth=0.53, relheight=0.15)

        self.type_text.pack(fill="both")

        send_button = Button(self.application_window, text="Send", command=lambda: self.send_message())
        send_button.place(relx=0.87, rely=0.755, relwidth=0.1, relheight=0.1)
        self.lb1.place(relwidth=0.9, relheight=0.95, relx=0.05, rely=0.03)
        self.chat_text.pack(fill='both')
        self.application_window.mainloop()

    def add_contacts(self, nicks):
        i = 0
        for nick in nicks:
            self.lb1.insert(i, nick)
            i += 1


    def send_message(self):
        self.type_message = self.type_text.get(1.0, END)
        try:
            self.s.send(self.nickname.encode('utf-8')
                        + ": ".encode('utf-8')
                        + self.type_message.encode('utf-8'))
        except socket.error:
            print("Can't send because no connection")
            self.type_text.delete(1.0, END)
            self.type_message = ""
            messagebox.showerror("Send error", "Can't send because no connection")
        else:
            self.type_message = ""
            self.chat_text.config(state="normal")
            self.chat_text.insert(INSERT, self.type_message)
            self.chat_text.config(state="disabled")
            self.type_text.delete(1.0, END)

    def run_thread(self):
        receive_thread = threading.Thread(target=self.receive())
        receive_thread.daemon = True
        receive_thread.start()
import log
import network
import chat
import threading
import tkinter as tk
import time


def send():
    while True:
        time.sleep(1)
        network.s.send(chat.type_message.encode())


def recv():
    while True:
        time.sleep(0.5)
        data = network.s.recv(1024)
        chat.chat_text.config(state="normal")
        chat.chat_text.insert(tk.INSERT, data)
        chat.chat_text.config(state="disabled")


nicks = ["seifer", "dima"]
network = network.Network()
log = log.Log(network.s, network.connected)


log.window()
nick = network.s.recv(1024)
chat = chat.Chat(network.s, nick.decode())
chat.add_contacts(nicks)
send_thread = threading.Thread(target=send)
send_thread.daemon = True
send_thread.start ()
receive_thread = threading.Thread(target=recv)
receive_thread.daemon = True
receive_thread.start()
chat.window()



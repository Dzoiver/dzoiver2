import socket
import threading
import sqlite3

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 9999))
sock.listen(1)
print("Server is started")
connections = []
client_number = 1


def handler(c, a):
    print("handler started")
    while True:
        global connections
        try:
            data = c.recv(1024)
        except socket.error:
            connections.remove (c)
            c.close ()
            print ("Breaking out of handler")
            break
        for connection in connections:
            try:
                connection.send(data)
            except socket.error:
                print("Breaking out of handler")
                connections.remove(c)
                c.close()
                break
        if not data:
            connections.remove(c)
            c.close()
            break


def database(c):
    global data
    conn = sqlite3.connect('dzoiver.db')
    curs = conn.cursor()
    while True:
        data = c.recv(1024)
        if data.decode() == "scc":
            break
        nck = data[3:].decode()
        data = c.recv(1024)
        pss = data[3:].decode()
        print ("nck = " + nck)
        print ("pss = " + pss)
        print("data = " + data.decode())
        print("data[2:3]" + str(data[2:3].decode()))
        if data[2:3].decode() == "q":
            curs.execute("SELECT * FROM users WHERE nickname='{}' AND password='{}'".format(nck, pss))
            fetch = curs.fetchone()
            print("fetch = " + str(fetch))
            if fetch is None:
                data = "err".encode()
            else:
                data = "rsl".encode()
        if data[2:3].decode() == "k":
            print("Searching for match")
            curs.execute("SELECT * FROM users WHERE nickname='{}'".format(nck))
            fetch = curs.fetchone()
            print("fetch = " + str(fetch))
            if fetch is None:
                curs.execute("INSERT INTO users (nickname, password) VALUES ('{}', '{}')"
                                  .format(nck, pss))
                conn.commit()
                data = "rsl".encode()
            else:
                data = "ern".encode()
        print("data = " + data.decode())
        c.send(data)
    return nck


while True:
    print("Waiting fo the client...")
    c, a = sock.accept()
    print("Client number: " + str(client_number))
    client_number += 1
    print(a, " has connected!")
    data = database(c)
    c.send(data.encode())
    connections.append(c)
    cThread = threading.Thread(target=handler, args=(c,a))
    cThread.daemon = True
    cThread.start()

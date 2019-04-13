import tkinter


class Log:
    def __init__(self, s, network):
        self.HEIGHT = 170
        self.WIDTH = 240
        self.nickname = ""
        self.logWindow = tkinter.Tk ()
        self.canvas = tkinter.Canvas (self.logWindow,
                                      height=self.HEIGHT,
                                      width=self.WIDTH)
        self.logButton = tkinter.Button (self.canvas, text="Log in",
                                         command=lambda: self.change (),
                                         width=12)
        self.enterButton = tkinter.Button(self.logWindow, text="Enter",
                                           command=lambda: self.enter ())
        self.nickEntry = tkinter.Entry(self.canvas)
        self.passEntry = tkinter.Entry(self.canvas, show="*")
        self.label = tkinter.Label(self.canvas, text="Registration")
        self.errorLabel = tkinter.Label(self.canvas, text="")
        self.mode = 0
        self.s = s
        self.network = network
        self.result = ""

    def window(self):
        self.canvas.pack()
        self.logButton.place(relx=0.6, rely=0.1)
        self.enterButton.place(relx=0.4, rely=0.65)
        self.nickEntry.place(relx=0.2, rely=0.3)
        self.passEntry.place(relx=0.2, rely=0.5)
        self.label.place(relx=0.2, rely=0.1)
        self.errorLabel.place(relx=0.1, rely=0.8)
        if not self.network:
            self.errorLabel.config(text="No connection", fg="red")
        self.logWindow.title("Dzoiver")
        self.logWindow.mainloop()

    def change(self):
        if self.mode == 0:
            self.label.config (text="Log in")
            self.logButton.config (text="Registration")
            self.mode = 1
        elif self.mode == 1:
            self.label.config (text="Registration")
            self.logButton.config (text="Log in")
            self.mode = 0

    def enter(self):
        global result
        if self.network:
            if len(self.nickEntry.get()) < 3 or len(self.nickEntry.get()) > 15 or len(
                    self.passEntry.get()) < 3 or len(self.passEntry.get()) > 15:
                self.nickname = self.nickEntry.get()
                self.errorLabel.config(text="Incorrect length", fg="red")
            else:
                self.enterButton.config(state='disabled')
                if self.mode == 0:  #registration
                    self.s.send("nck".encode()+self.nickEntry.get().encode())
                    self.s.send("psk".encode()+self.passEntry.get().encode())
                else:  # log in
                    self.s.send ("ncq".encode () + self.nickEntry.get ().encode ())
                    self.s.send ("psq".encode () + self.passEntry.get ().encode ())
                result = self.s.recv(1024)
                print("result = " + result.decode())
                if result[0:3].decode() == "err":
                    self.errorLabel.config (text="Nickname or password is wrong", fg="red")
                    print ("Error")
                    self.enterButton.config (state='normal')
                    result = ""
                elif result[0:3].decode() == "ern":
                    self.errorLabel.config (text="Nickname is already exists", fg="red")
                    print ("Error")
                    self.enterButton.config (state='normal')
                    result = ""
                elif result[0:3].decode() == "rsl":
                    self.s.send("scc".encode())
                    self.errorLabel.config (text="Success", fg="green")
                    print ("goodbye acc1")
                    self.success = True
                    self.enterButton.config (state='normal')
                    self.logWindow.destroy()
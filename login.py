from network import Network
from tkinter import *
from sender import MessageSender
class Login(Frame):
    def __init__(self,win,network:Network,sender:MessageSender):
        super().__init__(win)
        self.__net = network
        self.__createComponents()
        self.__sender = sender
    def __createComponents(self):
        self.__textbox = Text(self, width=40, height=1)
        self.__name = StringVar(value="Enter your name")
        self.__label = Label(self, textvariable=self.__name)
        self.__login_btn = Button(self, text="Login", command=self.__handleLogin)
        self.__label.grid(row=0, column=0)
        self.__textbox.grid(row=1, column=0, columnspan=2,padx=10)
        self.__login_btn.grid(row=1, column=2)

    def __handleLogin(self):
        username = self.__textbox.get("1.0", "end-1c")
        self.__net.registerUser(username)
        user = self.__net.getUser()
        if not user:
            self.setLabel("Username already taken")
        else:
            self.setLabel(username)
            self.__textbox.configure(state="disabled")
            self.__login_btn.configure(state="disabled")
            self.__sender.enableBtn()
    def setLabel(self,text):
        self.__name.set(text)

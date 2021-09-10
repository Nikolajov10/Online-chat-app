from tkinter import *
from network import Network
from login import Login
from contacts import Contacts
from sender import MessageSender
from chat import Chat
from user import User,Message
class App():
    HEIGHT = 470
    WIDTH = 570
    def __init__(self,network:Network):
        self.__root = Tk()
        self.__root.title = "Chat App"
        self.__root.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.__net = network
        self.__createWindow()
    def __createWindow(self):
        self.__sender = MessageSender(self.__root, self.__net)
        self.__sender.grid(row=7, column=0, columnspan=4, pady=5)
        self.__login = Login(self.__root,self.__net,self.__sender)
        self.__login.grid(row=0,column=0,columnspan=3,padx=5,pady=5)
        self.__contacts = Contacts(self.__root,self.__sender,self.__net)
        self.__contacts.grid(row=0,column=3,rowspan=3,padx=5,pady=5)
        self.__chat_screen = Chat(self.__root)
        self.__chat_screen.grid(row=1,column=0,rowspan=6,columnspan=3)

    def updateApp(self,user:User):
        contact = self.__contacts.getContact()
        if contact:
            history = user.getHistory(contact)
            self.__chat_screen.drawMsg(history,contact)


    def getSender(self):
        return self.__sender
    def start(self):
        loged = False
        while True:
            try:
                user:User = self.__net.getUser()
                if user:
                    self.updateApp(user)
                    if not loged:
                        loged = True
                        self.__contacts.turnOn()
                        self.__contacts.setUser(user)
                self.__root.update_idletasks()
                self.__root.update()
            except:
                break
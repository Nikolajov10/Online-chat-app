from tkinter import *
from network import Network

class MessageSender(Frame):
    def __init__(self,win,net:Network):
        super().__init__(win)
        self.__net = net
        self.__createComponents()
        self.__send_to = None
    def __createComponents(self):
        self.__input_msg = Text(self,height=2,width=50)
        self.__input_msg.grid(row=0,column=0,columnspan=3,padx=5)
        self.__send_btn = Button(self,text = "Send message",command=self.sendMessage\
                                 ,state="disabled")
        self.__send_btn.grid(row=0,column=3,ipady=5)

    def setSendCont(self,cont):
        self.__send_to = cont

    def sendMessage(self):
        msg = self.__input_msg.get("1.0", "end-1c")
        self.__input_msg.delete("1.0", "end-1c")
        if self.__send_to:
            self.__net.sendMsg(msg,self.__send_to)

    def enableBtn(self):
        self.__send_btn.config(state="active")

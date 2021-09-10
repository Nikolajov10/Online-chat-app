from tkinter import *
from user import Message
class Chat(Frame):
    MAX_MSG = 16
    def __init__(self,win:Tk):
        super().__init__(win, width=300, height=300)
        #self.pack(expand=True, fill=BOTH)
        self.__canvas = Canvas(self, bg='lime', width=300, height=300, scrollregion=(0, 0, 500, 500))
        hbar = Scrollbar(self, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=self.__canvas.xview)
        vbar = Scrollbar(self, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=self.__canvas.yview)
        self.__canvas.config(width=300, height=300)
        self.__canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.__canvas.pack(side=LEFT, expand=True, fill=BOTH)
        self.__current_pos = 0


    def drawMsg(self,history:list[Message],contact:str):
        self.__canvas.delete("all")
        if not history:
            return
        start = 0
        n = len(history)
        if n>Chat.MAX_MSG:
            start = n - Chat.MAX_MSG
        for i in range(start,n) :
            msg = history[i]
            side = 0 if msg.sender == contact else 1
            text_msg = msg.text
            color = "blue"
            if side == 0:
                color = "red"
            width =self.__canvas.winfo_width()
            height = self.__canvas.winfo_height()
            offset = 5
            if side == 1:
                offset*= -1
            self.__canvas.create_text(offset + len(text_msg)*6 + side*(width-len(text_msg)*7),30*(self.__current_pos)+8,\
                                anchor=E,text=text_msg,fill=color)
            self.__current_pos += 1
        self.__current_pos = 0



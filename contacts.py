from  tkinter import *
from sender import MessageSender
import  app
from user import User
from network import Network
import mongoDb
from sysVar import *

class Contacts(Frame):
    def __init__(self,win:Tk,sender:MessageSender,net:Network,usr:User=None):
        super().__init__(win)
        self.__root = win
        self.__contacts = []
        self.__sender = sender
        self.__net = net
        if  usr:
            self.__contacts = usr.getContacts().copy()
        else:
            self.__contact = None
        self.__user = usr
        self.__createComponents()

    def __createComponents(self):
        self.__label = Label(self, text="CONTACTS:")
        self.__label.grid(row=0,column=0)
        scrollbar = Scrollbar(self)
        scrollbar.grid(row=1,column=1,rowspan=2,ipady=40)
        self.__list = Listbox(self,yscrollcommand=scrollbar.set)
        self.__list.grid(row=1,column=0,rowspan=2)
        self.__list.bind("<<ListboxSelect>>",self.__selectContact)
        for ind,contact in enumerate(self.__contacts):
            self.__list.insert(END,contact)
            self.__list.itemconfig(ind, bg="lightyellow" if ind % 2 == 0 else "lime")
        scrollbar.config(command = self.__list.yview)
        self.__addbtn = Button(self,text="Add contact",command=self.__addContact,state="disabled")
        self.__addbtn.grid(row=3)
        self.__contact_label = Label(self,text="Selected contact:",fg="red")
        self.__contact_label.grid(row=4)

    def turnOn(self):
        self.__addbtn.config(state="active")

    def setUser(self,usr:User):
        self.__user = usr
        conts = self.__user.getContacts()
        for index,cont in enumerate(conts):
            self.__list.insert(END, cont)
            self.__list.itemconfig(index,bg="lightyellow" if index % 2 == 0 else "lime")
            self.__contacts.append(cont)

    def __selectContact(self,event):
        try:
            selection = event.widget.curselection()
            self.__sender.setSendCont(self.__contacts[selection[0]])
            self.__contact = self.__contacts[selection[0]]
            self.__contact_label.configure(text="Selected contact:"+str(self.__contacts[selection[0]]))
        except:
            pass
    def getContact(self):
        return self.__contact

    def __handleContactAdding(self):
        name = self.__input_cont.get("1.0", "end-1c")
        self.__contacts.append(name)
        self.__list.insert(END, name)
        self.__list.itemconfig(len(self.__contacts) - 1, bg="lightyellow" if (len(self.__contacts)-1) % 2 == 0 else "lime")
        if self.__user:
            self.__user.insertContact(name)
            self.__net.sendMsg(UPDATE_USER,None,self.__user.getContacts())
        self.__dialog.destroy()

    def __createDialog(self):
        self.__dialog = Toplevel()

        x = self.__root.winfo_x()
        y = self.__root.winfo_y()
        w = self.__dialog.winfo_width()
        h = self.__dialog.winfo_height()
        self.__dialog.geometry("%dx%d+%d+%d" % (w, h, x + x//2, y + y//2))

        self.__dialog.title("Add Contact")
        self.__dialog.geometry(f"{app.App.WIDTH//4}x{app.App.HEIGHT // 4}")
        label = Label(self.__dialog,text = "Enter contact name:")
        label.pack(side=TOP)
        btn = Button(self.__dialog, text="Add",command=self.__handleContactAdding)
        btn.pack(side=BOTTOM)
        self.__input_cont = Text(self.__dialog,width=30,height=2)
        self.__input_cont.pack(side=BOTTOM)

    def __addContact(self):
        self.__createDialog()
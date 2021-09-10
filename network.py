from sysVar import *
import  pickle
from user import wrapperUser
class Network:
    def __init__(self):
        self.__client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__user_id = None
        self.__id = int(self.__connect())

    def getId(self):
        return self.__id
    def getUserId(self):
        return self.__user_id

    def __connect(self):
        try:
            self.__client.connect(ADDR)
            msg_len = self.__client.recv(HEADER).decode(FORMAT)
            if msg_len:
                msg = self.__client.recv(int(msg_len)).decode(FORMAT)
                return msg
        except socket.error as e:
            print(e)

    def sendMsg(self,msg,send_to,contacts=None):
        try:
            msg = msg.encode(FORMAT)
            msg_len = str(len(msg)).encode(FORMAT)
            if msg_len:
                msg_len += b" " * (HEADER - len(msg_len))
                self.__client.send(msg_len)
                self.__client.send(msg)
                usr = wrapperUser("",self.__user_id,send_to)
                if contacts:
                    usr.setContacs(contacts)
                self.__client.sendall(pickle.dumps(usr))
        except socket.error as e:
            print(e)

    def registerUser(self,name):
        try:
            msg = REGISTER_MESSAGE.encode(FORMAT)
            msg_len = str(len(msg)).encode(FORMAT)
            if msg_len:
                msg_len += b" " * (HEADER - len(msg_len))
                self.__client.send(msg_len)
                self.__client.send(msg)
                usr = wrapperUser(name,self.__id,None)
                self.__client.sendall(pickle.dumps(usr))
                msg_len = self.__client.recv(HEADER).decode(FORMAT)
                if msg_len:
                    msg = self.__client.recv(int(msg_len)).decode(FORMAT)
                    if msg != USER_NOT_FOUND:
                        self.__user_id = int(msg)
        except socket.error as e:
            print(e)

    def getUser(self):
        if not self.__user_id:
            return None
        try:
            msg = GET_USER_MESSAGE.encode(FORMAT)
            msg_len = str(len(msg)).encode(FORMAT)
            if msg_len:
                msg_len += b" " * (HEADER - len(msg_len))
                self.__client.send(msg_len)
                self.__client.send(msg)
                usr = wrapperUser("", self.__user_id,None)
                self.__client.sendall(pickle.dumps(usr))
                recv_len = self.__client.recv(HEADER).decode(FORMAT)
                if recv_len:
                    msg = self.__client.recv(int(recv_len)).decode(FORMAT)
                    if msg != FOUND_USER_MESSAGE:
                        return None
                    return pickle.loads(self.__client.recv(2048))
        except socket.error as e:
            print(e)

class wrapperUser:
    def __init__(self,name,id,send_to):
        self.name = name
        self.id = id
        self.send_to = send_to
        self.contacts = []
    def setContacs(self,conts):
        self.contacts = conts.copy()

class Message:
    def __init__(self,msg,sender_name):
        self.text = msg
        self.sender = sender_name
    @staticmethod
    def messageToDocument(msg) -> dict:
        """
        Parser for MongoDB to convert message to Document Object
        :return: dict {"Text":self.text,"Sender"self.sender}
        """
        doc = {
            "Text" : msg.text,
            "Sender" : msg.sender
        }
        return doc
    @staticmethod
    def documentToMessage(doc:dict):
        """

        :param doc: dict - MongoDB document
        :return: Message
        """
        return Message(doc["Text"],doc["Sender"])
class User:
    def __init__(self,name,id,hist=dict()):
        self.__name = name
        self.__id = id
        self.__history = hist # key is other user name , value will be list of messages with that user
        self.__contacts = []
    def __str__(self):
        return f"[{self.__id}] {self.__name}"

    def insertMessage(self,message:Message,contact:str):
        if contact not in self.__history:
            self.__history[contact] = [message]
        else:
            self.__history[contact].append(message)

    def getHistory(self,contact=None):
        if not contact:
            # special case needed for MongoDB
            d = dict()
            for key in self.__history.keys():
                d[key] = self.__history[key].copy()
                for index in range (len(d[key])):
                    d[key][index] = Message.messageToDocument(d[key][index])
            return d

        if contact in self.__history:
            return self.__history[contact]
        return None

    def getContacts(self):
        return self.__contacts

    def addContact(self,cont):
        self.__contacts.append(cont)

    def setContacts(self,conts:list[str]):
        self.__contacts = conts.copy()

    def insertContact(self,cont:str):
        self.__contacts.append(cont)

    def getName(self):
        return self.__name

    def getId(self):
        return self.__id

import pymongo
from pymongo import MongoClient
from user import User,Message

""" Document structure : User
{
        "_id":id,
        "Name":name,
        "Contacts":[names...],
        "History" : dict(key:[Messages...])
        Problem : Can't store object in Messages format ->
        Messages{fileds:text,sender} -> 
        {
            "Text":text,
            "Sender": sender
        }
        need to implement parser for converting Messages to Document structure and vice versa 
        
}"""

class MongoDb:
    client = None
    db = None
    collection:pymongo.collection.Collection= None

    @staticmethod
    def initDB():
        if not MongoDb.client:
            MongoDb.client = MongoClient("mongodb+srv://test:test@cluster0.xnnul.mongodb.net/ChatApp?retryWrites=true&w=majority")
        if not MongoDb.db:
            MongoDb.db = MongoDb.client["ChatApp"]
        if not MongoDb.collection:
            MongoDb.collection = MongoDb.db["Users"]

    @staticmethod
    def insertUser(usr:User):
        post = {
            "_id":usr.getId(),
            "Name": usr.getName(),
            "History":usr.getHistory(),
            "Contacts":usr.getContacts()
        }
        MongoDb.collection.insert_one(post)

    @staticmethod
    def updateUser(usr:User):
        MongoDb.collection.update_one({"_id":usr.getId()},{"$set":{"History":usr.getHistory(),"Contacts":usr.getContacts()}})

    @staticmethod
    def getAllUsers():
        results = MongoDb.collection.find({})
        users = {}
        id = 0
        for res in results:
            hist = res["History"]
            for key in hist.keys():
                for index,msg in enumerate(hist[key]):
                    hist[key][index] = Message.documentToMessage(msg)
            usr = User(res["Name"],res["_id"],hist)
            usr.setContacts(res["Contacts"])
            users[usr.getId()] = usr
            id = max(id,int(usr.getId()))
        return users,id

#MongoDb.initDB()
#usr = User("Asis",2,{"Nikola":[]})
#MongoDb.insertUser(usr)
#MongoDb.updateUser(usr)
#MongoDb.collection.delete_many({})
#print(MongoDb.getAllUsers())

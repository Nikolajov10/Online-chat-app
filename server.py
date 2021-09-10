from sysVar import *
import pickle
import threading
from user import *
from mongoDb import MongoDb

def sendMessage(msg:str,conn:socket):
    # TODO
    message = msg.encode(FORMAT)
    message_len = len(message)
    message_len = str(message_len).encode(FORMAT)
    message_len += b" " * (HEADER - len(message_len))
    conn.send(message_len)
    conn.send(message)

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

MongoDb.initDB()

users,id = MongoDb.getAllUsers()
print("Users registred in system:")
for usr_key in users:
    print(users[usr_key])
active_users = {}
net_id = 0

def handle_client(conn:socket,addr):
    print(f"[NEW CONNECTION] {addr} connected...")
    global id,net_id
    net_id += 1
    my_id = net_id
    sendMessage(str(my_id),conn)
    connected = True
    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg = conn.recv(int(msg_len)).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                wrap_usr = pickle.loads(conn.recv(2048))
                del active_users[wrap_usr.id]
                break
            elif msg == REGISTER_MESSAGE:
                wrap_usr = pickle.loads(conn.recv(2048))
                name_taken = False
                for key in active_users.keys():
                    if active_users[key].getName() == wrap_usr.name:
                        name_taken = True
                        break
                if not name_taken:
                    usr_id = None
                    for key in users.keys():
                        if users[key].getName() == wrap_usr.name:
                            usr_id = key
                            break
                    usr = None
                    if not usr_id:
                        usr = User(wrap_usr.name,id+1)
                        id += 1
                        users[id] = usr
                        print(f"Inserting {usr} to databse")
                        MongoDb.insertUser(usr)
                    else:
                        usr = User(wrap_usr.name,usr_id)
                    active_users[usr.getId()] = usr
                    sendMessage(str(usr.getId()),conn)
                    print("New User:"+str(active_users[usr.getId()]))
                else:
                    sendMessage(USER_NOT_FOUND,conn)
                    print(f"Username {wrap_usr.name} already taken!")
            elif msg == GET_USER_MESSAGE:
                usr = pickle.loads(conn.recv(2048))
                msg = usr.id
                if msg in users:
                    sendMessage(FOUND_USER_MESSAGE,conn)
                    conn.send(pickle.dumps(users[msg]))
                else:
                    sendMessage(USER_NOT_FOUND,conn)
            elif msg == UPDATE_USER:
                usr = pickle.loads(conn.recv(2048))
                user = active_users[usr.id]
                user.setContacts(usr.contacts)
                users[usr.id] = user
                MongoDb.updateUser(user)
            else:
                usr = pickle.loads(conn.recv(2048))
                user = users[usr.id]
                user2 = None
                for u in users.keys():
                    if users[u].getName() == usr.send_to:
                        user2 = users[u]
                        break
                if user2 != None:
                    _msg = Message(msg,user.getName())
                    user.insertMessage(_msg,user2.getName())
                    user2.insertMessage(_msg,user.getName())
                    MongoDb.updateUser(user)
                    MongoDb.updateUser(user2)
                print(str(user) + " sending msg to "+str(user2) + " : " + msg )
    conn.close()


def start():
    server.listen()
    print("[LISTENING] Server starts listening on " +str(SERVER))
    while True:
        conn,addr =server.accept()
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print("Active connections" + str(threading.activeCount() - 1))



print("[STARTING] Server starting...")
start()

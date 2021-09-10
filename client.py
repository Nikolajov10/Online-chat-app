from network import Network
from sysVar import *
from app import App

net = Network()
App(net).start()
net.sendMsg(DISCONNECT_MESSAGE,None)
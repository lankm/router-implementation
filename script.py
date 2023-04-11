# README
#
# Author: Landon Moon, Tsebaot Meron
#
# I think this is wrong btw

import socket
import threading
from time import *
import sys
import os

# classes =====================================================================
class Router:
    label = ""
    IP = ""
    conns = {}

    def __init__(self, label, IP):
        self.label = label
        self.IP = IP
        self.conns = {}

    def run(self):
        #TODO
        return
    
    def display(self):
        print("label:", self.label)
        print("IP:", self.IP)
        print("Conns:", self.conns)
# functions ===================================================================
# main ========================================================================

# Command line arguments
if len(sys.argv)<2:
    print("ERR. Expected:\"script.py PORT\"")
    os._exit(1)
port = int(sys.argv[1])

# Input config file date
configFile = open(".config", "r")

routers = []

while (line:=configFile.readline().strip()) != "":
    tokens = line.split()
    routers.append( Router(tokens[1], tokens[0]) )

while (line:=configFile.readline().strip()) != "":
    tokens = line.split()
    print(tokens)
    for r in routers:
        if r.label == tokens[0]:
            r.conns[tokens[1]] = tokens[2]
        if r.label == tokens[1]:
            r.conns[tokens[0]] = tokens[2]

# activate routers
for r in routers:
    Athread = threading.Thread(target=r.run(), args=())
    Athread.start()

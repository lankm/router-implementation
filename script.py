# README
#
# Author: Landon Moon, Tsebaot Meron

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
        self.display()
        return
    
    def display(self):
        print("label:", self.label)
        print("IP:", self.IP)
        print("Conns:", self.conns)
# functions ===================================================================
# main ========================================================================

# Command line arguments
if len(sys.argv)<2:
    print("ERR. Expected:\"script.py PORT LABEL\"")
    os._exit(1)
port = int(sys.argv[1])
router = sys.argv[2]

# Input config file date
configFile = open(".config", "r")

routers = []

while (line:=configFile.readline().strip()) != "":
    tokens = line.split()
    routers.append( Router(tokens[1], tokens[0]) )

while (line:=configFile.readline().strip()) != "":
    tokens = line.split()
    for r in routers:
        if r.label == tokens[0]:
            r.conns[tokens[1]] = tokens[2]
        if r.label == tokens[1]:
            r.conns[tokens[0]] = tokens[2]

# activate routers
for r in routers:
    if r.label == router:
        Athread = threading.Thread(target=r.run(), args=())
        Athread.start()

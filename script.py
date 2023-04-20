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
    def __init__(self, label, IP, port):
        # basic info
        self.label = label
        self.IP = IP
        self.port = port

        # connection info
        self.conns = {}
        self.DV = {}

        # threading value
        self.running = True

    def run(self):
        self.display()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.IP, self.port))

        reader = threading.Thread(target=self.reader, args=(sock,))
        reader.start()
        sender = threading.Thread(target=self.sender, args=(sock,))
        sender.start()

        # sleep until ^C is encountered
        try:
          while True:
            sleep(1)
        except KeyboardInterrupt:
          self.running = False
          reader.join()
          sender.join()
          sock.shutdown(socket.SHUT_RDWR)
          print('Router shutdown.')
    
    def reader(self, sock):
        while self.running:
            try:
                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                print("reader: %s" % data)
            except ConnectionResetError:
                print("reader: no data")
            sleep(1)
        return
    
    def sender(self, sock):
        while self.running:
            for ip in self.conns.keys():
                sock.sendto(b"data", (ip, self.port))
            print("sender")
            sleep(1)
        return
    
    def display(self):
        print("label:", self.label)
        print("IP:", self.IP)
        print("port:", self.port)
        print("conns:", self.conns)
# functions ===================================================================
def findIP(routers, label):
    for r in routers:
        if r.label == label:
            return r.IP
# main ========================================================================
def main():
    
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
      routers.append( Router(tokens[1], tokens[0], port) )

  while (line:=configFile.readline().strip()) != "":
      tokens = line.split()
      for r in routers:
          if r.label == tokens[0]:
              r.conns[findIP(routers,tokens[1])] = tokens[2]
          if r.label == tokens[1]:
              r.conns[findIP(routers,tokens[0])] = tokens[2]

  # activate routers
  for r in routers:
      if r.label == router:
          r.run()
  
  return

if __name__ == "__main__":
    main()

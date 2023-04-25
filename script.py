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
             #run the dv over here 
            self.Distance_vector()
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




    def Distance_vector(self):
        for ip,weight in self.conns.items():
            self.DV[ip]=int(weight)

        #this is checking for convergence 
        while True:
            temp=dict(self.DV)

            for node in self.conns.keys():
                
                #sending the dv to the next node 
                data= f'{self.IP}:{self.DV}'.encode('utf-8')
                sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                sock.sendto(data,(node,self.port))
                sock.close()
                """
                #getting information from node 
                sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                sock.bind((self.IP,self.port))
                sock.listen(5)
                sock.settimeout(2)
                """
                nodeDV=0
                try:
                    data,addr = sock.recvfrom(1024)
                    nodeDV=eval(data.decode()) #this is the neighbors info
                except:
                    nodeDV={nodeDV: float("inf")} #this is if it times out
                sock.close()

                for ip,weight in nodeDV.items():
                    if ip == self.IP:
                        continue
                    if ip not in self.conns.keys():
                        continue
                    if ip not in self.DV.keys():
                        self.DV[ip]=float("inf")
                    if weight + self.conns[node] < self.DV[ip]:
                        self.DV[ip]= weight + self.conns[node]

            if temp == self.DV:
                break

        print("DV for router %s:" % self.label)
        for ip,weight in self.DV.items():
            print(ip,weight)
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

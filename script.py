# README
#
# Author: Landon Moon, Tsebaot Meron

from datetime import datetime
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

        # runtime info
        self.updateAmt = 0

    def run(self):
        self.displayinit()

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
            #self.Distance_vector()
        except KeyboardInterrupt:
          self.displayfinal()
          print('Router shutdown.')
          os._exit(1) # OS._exit reliquished the owned ports
    
    def reader(self, sock):
        while True:
            try:
                # recieve message
                data, addr = sock.recvfrom(1024)
                if addr[0] == self.IP:
                    continue
                if addr[0] not in self.conns.keys():  #local host is weird sometimes
                    continue
                
                # decode and parse
                data = data.decode()
                #print(f'== from:{addr[0]} ==')
                for data in data.split(','):
                    toIP = data.split(' ')[0]
                    dist = int(data.split(' ')[1]) + self.conns[addr[0]]
                    #print(f'to:{toIP} - dist:{dist}')

                    # change DV values
                    tempDV = self.DV.copy()
                    matched = False
                    for ip, weight in tempDV.items():
                        # get minimum if exist
                        if toIP == ip:
                            minimum = min(weight, dist)

                            # if DV value is changed
                            if minimum != weight:
                                print(f'Changed DV entry: {toIP} - {tempDV[toIP]} => {toIP} - {dist}')
                                self.updateAmt += 1

                            # if ip match was found
                            self.DV[toIP] = minimum
                            matched = True
                    # enter entry if doesn't already exist
                    if not matched:
                      print(f'Added DV entry:   {toIP} - {dist}')
                      self.updateAmt += 1
                      self.DV[toIP] = dist
                      
                
                    
            except ConnectionResetError:
                pass
        return
    
    def sender(self, sock):
        while True:
            # construct format for DV
            data = ''
            for dest, dist in self.DV.items():
                data += f'{dest} {dist},'
            data = data[:-1] # remove final comma

            # send DV to all connections
            for ip in self.conns.keys():
                sock.sendto(data.encode(), (ip, self.port))
            sleep(1)
        return
    
    def displayinit(self):
        print("== label: %s IP: %s Port: %s ==" % (self.label, self.IP, self.port))
        print("conns:", self.conns)
        print()
        return
    
    def displayfinal(self):
        print()
        print("== %s %s %s ==" % (self.label, self.IP, self.port))
        print('ID: 1001906270 and 1001629719')
        print(f'Date and time: %s' % (datetime.now()))
        print(f'Total updates: {self.updateAmt}')
        print('-- final DV --')
        for key, value in self.DV.items():
            print(f'  IP: {key}   DIST: {value}')
        print()
        return
    

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
  #print(configFile.read())--------------THIS PRINTS OUT CONFIG FOR ALL ROUTERS

  routers = []

  # creating routers
  while (line:=configFile.readline().strip()) != "":
      tokens = line.split()
      routers.append( Router(tokens[1], tokens[0], port) )

  # setting connection info
  while (line:=configFile.readline().strip()) != "":
      tokens = line.split()
      for r in routers:
          # if A -> B
          if r.label == tokens[0]:
              ip = findIP(routers,tokens[1])
              r.conns[ip] = int(tokens[2])
          # if B -> A
          if r.label == tokens[1]:
              ip = findIP(routers,tokens[0])
              r.conns[ip] = int(tokens[2])
          r.conns[r.IP] = 0
          r.DV = r.conns  # DV = conns initially

  # activate router
  for r in routers:
      if r.label == router:
          r.run()
  
  return

if __name__ == "__main__":
    main()

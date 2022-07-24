#! /opt/homebrew/bin/python3

from Server import createServer
import sys

server = createServer()


if __name__ == "__main__":
   if len(sys.argv) == 1:
      server.mainloop() 
   elif len(sys.argv) == 2:
      if sys.argv[1] == "passiv":
         server.run_passiv()
      elif sys.argv[1] == "listen":
         server.listen_to()
      elif sys.argv[1] == "database":
         server.database_config() 
      elif sys.argv[1] == "cam":
         server.handleCam()
      else:
         print("No such argv option => %s" % sys.argv[1])
         
      
   else:
      print("Only zero or one argv allowed")
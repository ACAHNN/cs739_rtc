import sys
import time
from datetime import datetime
from chatbot import ChatBot


if __name__ == '__main__':
    roundTripMessageTimes = []
    # create a chatbot instance
    cb1 = ChatBot(True)
  
    if not sys.argv[1]:
      print "Need argument for site to visit (local or app-engine remot)"
      sys.exit()  
  
    if not sys.argv[2]:
      print "Need argument as to which user to login as"
      sys.exit()
    
    if not sys.argv[3]:
      print "Need password of the user to login"
      sys.exit()
    
    if not sys.argv[4]:
      print "Need length of time to run logging"
      sys.exit()
      
    # navigate to the chat site
    cb1.visit(sys.argv[1])

    # enter the site
    cb1.login(sys.argv[2], sys.argv[3])

    # add a non-existent friend
   # cb1.add_friend('bob1')

    # select the current freinds list
    friends = cb1.get_friends_list()
    aFriend = friends[0]
    # iterate through the friends list
  
    # select friend chat window
    cb1.select_friend(aFriend)
    
    startTime = time.clock()
    
    while time.clock() - startTime < sys.argv[4]:    
    
        # send a message    
      beforeSendTime = time.clock()
      currentChatLength = len(cb1.get_messages()) #INSERT CURRENT CHAT LENGTH
      cb1.send_message('qwerqwerwrreqr')
      
      while currentChatLength == len(cb1.get_messages()): #INSURT CURRENT CHAT LENGTH
        #DONOTHIGN
        nothing = 3
        
      afterSendTime = time.clock()
      roundTripMessageTimes.append(afterSendTime - beforeSendTime)
    
      time.sleep(1)
    cb1.logout()
    # logout
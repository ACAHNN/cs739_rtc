import sys
import time
from datetime import datetime
from chatbot import ChatBot


if __name__ == '__main__':
    roundTripMessageTimes = []
    
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
      
    site = sys.argv[1]
    # create a chatbot instance
    cb1 = ChatBot(True, site, False)
  
      
    # navigate to the chat site
    cb1.visit(sys.argv[1] + '/login')

    # enter the site
    cb1.login(sys.argv[2], sys.argv[3])

    # add a non-existent friend
   # cb1.add_friend('bob1')

    # select the current freinds list
    friends = cb1.get_friends_list()
    while not friends:
        friends = cb1.get_friends_list()
    aFriend = friends[0]
    # iterate through the friends list
  
    # select friend chat window
    cb1.select_friend(aFriend)
    
    startTime = time.time()
    lastSecond = 0
    messagesSent = 1
    currentAverage = 0
    while ((time.time() - startTime) < int(sys.argv[4])):    
    #  print "time running ", time.time() - startTime, " time to run ", sys.argv[4]
        # send a message    
      currentChatLength = len(cb1.get_messages()) #INSERT CURRENT CHAT LENGTH
      beforeSendTime = time.time()
      cb1.send_message('qwerqwerwrreqr')
      
      while currentChatLength == len(cb1.get_messages()): #INSURT CURRENT CHAT LENGTH
        #DONOTHIGN
        nothing = 3
        
      afterSendTime = time.time()
      if afterSendTime - startTime < lastSecond + 1:
        messagesSent += 1
        currentAverage += afterSendTime - beforeSendTime
      else:
        currentAverage /= messagesSent
        messagesSent = 1
        lastSecond = lastSecond + 1
        roundTripMessageTimes.append(currentAverage)
        currentAverage = 0
      #roundTripMessageTimes.append(afterSendTime - beforeSendTime)
    
      #time.sleep(1)
      
    print roundTripMessageTimes
    cb1.logout()
    # logout
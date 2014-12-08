import sys
import time
from datetime import datetime
from chatbot import ChatBot


if __name__ == '__main__':

    # create a chatbot instance
    cb1 = ChatBot(False)
  
    if not sys.argv[1]:
      print "Need argument for site to visit (local or app-engine remot)"
      return  
  
    if not sys.argv[2]:
      print "Need argument as to which user to login as"
      return
    
    if not sys.argv[3]:
      print "Need password of the user to login"
      return
    # navigate to the chat site
    cb1.visit(sys.argv(1))

    # enter the site
    cb1.login(sys.argv[2], sys.argv[3])

    # add a non-existent friend
    cb1.add_friend('bob1')

    # select the current freinds list
    friends = cb1.get_friends_list()
    aFriend = friends[0]
    # iterate through the friends list
  
    # select friend chat window
    cb1.select_friend(aFriend)
    # send a message
    currentTime = time.clock()
    cb1.send_message('qwerqwerwrreqr')
    
    time.sleep(1)
    cb1.logout()
    # logout
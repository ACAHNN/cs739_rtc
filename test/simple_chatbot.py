import sys
import time

from chatbot import ChatBot


if __name__ == '__main__':

    # create a chatbot instance
    cb1 = ChatBot(False)

    # navigate to the chat site
    cb1.visit('http://real-time-chat.appspot.com/login')

    # enter the site
    cb1.login('aaron', '1234')

    # add a non-existent friend
    cb1.add_friend('bob1')

    # select the current freinds list
    friends = cb1.get_friends_list()

    # iterate through the friends list
    for friend in friends:
        # select friend chat window
        cb1.select_friend(friend)
        # send a message
        for i in range(0,5):
            cb1.send_message('qwertyuiopasadfghjklzxcvbnm')
            time.sleep(.5)

    # logout
    cb1.logout()

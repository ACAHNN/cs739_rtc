import sys
import time

from chatbot import ChatBot


if __name__ == '__main__':

    # create a chatbot instance
    site = 'localhost:8080'
    cb1 = ChatBot(False, site)

    # navigate to the chat site
    cb1.visit(site)

    # enter the site
    cb1.login('asdf', 'asdf')

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

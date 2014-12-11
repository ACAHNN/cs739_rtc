import sys
import time

from chatbot import ChatBot


if __name__ == "__main__":

    # create the bot
    qchatbot = ChatBot(False, 'http://real-time-chat.appspot.com/', True)
    
    # navigate to the login page
    qchatbot.visit(qchatbot.site)
    
    # login to the site
    qchatbot.login('aaron', '1234')
    
    # select the friend to talk with
    assert qchatbot.select_friend('alice'), "Your friend is offline"
    
    # quotes to respond with
    quotes, index = [], 0
    with open('quotes.txt', 'rb') as f:
        for line in f:
            quotes.append(line)
    
    # record the nubmer of messages
    num_messages = len(qchatbot.get_messages())
    
    while True:
        # indicates a message was recieved, respond
        if num_messages != len(qchatbot.get_messages()):
            qchatbot.send_message(quotes[index%len(quotes)].strip())
            num_messages = len(qchatbot.get_messages())
            index += 1

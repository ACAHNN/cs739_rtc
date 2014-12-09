import sys
import time

from selenium import webdriver
from pyvirtualdisplay import Display


class ChatBot:

    def __init__(self, use_vd, site, debug):
        self._init_vd(use_vd)
        self._init_webdriver()
        self.site = site
        self.debug = debug


    def __del__(self):
        if hasattr(self, 'wd'):
            self.wd.close()
        if hasattr(self, 'vd'):
            self.vd.stop()


    def _init_vd(self, use_vd):
        if use_vd:
            try:
                self.vd = Display(visible=0, size=(1920,1080))
                self.vd.start()
            except Exception as e:
                print e

        return None


    def _init_webdriver(self):
        self.wd = webdriver.Firefox()
        return None


    def visit(self, site):
        if self.debug:
          print "Task: chatbot visiting %s" % site
        self.wd.get(site)
        return None

        
    def login(self, username, password):
        if self.debug:
          print "Task: chatbot logging in -> username: %s password %s" % (username, password)

        element = self.wd.find_element_by_name('username')
        if element:
            element.send_keys(username)
        
        element = self.wd.find_element_by_name('password')
        if element:
            element.send_keys(password)
            element.submit()


    def logout(self):

        element = self.wd.find_element_by_partial_link_text('Setting')
        if element:
            element.click()
            element2 = self.wd.find_element_by_partial_link_text('Logout')
            if element2:
                element2.click()
                if self.debug:
                  print "Task: chatbot logged out"


    def create_account(self, name, username, password):
        if self.debug:
          print "Task: chatbot creating account -> username: %s password: %s" % (username, password)

        self.visit(self.site+'/signup')
        element = self.wd.find_element_by_name('name')
        if element:
            element.send_keys(name)

        element = self.wd.find_element_by_name('username')
        if element:
            element.send_keys(username)

        element = self.wd.find_element_by_name('password')
        if element:
            element.send_keys(password)

        element = self.wd.find_element_by_name('password1')
        if element:
            element.send_keys(password)
            element.submit()


    def add_friend(self, friend_name):

        self.visit(self.site+'/add_friend')
        
        element = self.wd.find_element_by_name('username')
        if element:
            element.send_keys(friend_name)
            element.submit()

        success = False
        if self.wd.current_url == self.site:
            if self.debug:
              print "Task: chatbot added friend: %s" % friend_name
            success = True
        else:
            if self.debug:
              print "Error: chatbot failed to add friend: %s" % friend_name

        self.visit(self.site)
        
        return success


    def get_friends_list(self):

        friends = []
        elements = self.wd.find_elements_by_class_name('friend')
        for element in elements:
            friends.append(element.text)

        return friends

    def select_friend(self, friend_name):

        elements = self.wd.find_elements_by_class_name('friend')
        for element in elements:
            if element.text == friend_name:
                if self.debug:
                  print "Task: chatbot selected friend: %s to chat with" % friend_name 
                element.click()


    def get_messages(self):
        
        elements = self.wd.find_elements_by_class_name("message")
        return elements
    
    def send_message(self, msg):

        element = self.wd.find_element_by_id('msg_form')
        if element:
            if self.debug:
              print "Task: chatbot sent msg: %s" % msg
            element.send_keys(msg)
            element.submit()
        else:
            print "Error: chatbot failed to send msg: %s" % msg


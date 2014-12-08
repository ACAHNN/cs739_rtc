#!/usr/bin/env python

# Real-time Chat Server

import logging
import os.path
import webapp2
import json
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from google.appengine.api import channel
from webapp2_extras import auth
from webapp2_extras import sessions
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError

from models import User
from models import FriendList

def user_required(handler):
  """
    Decorator that checks if there's a user associated with the current session.
    Will also fail if there's no session present.
  """
  def check_login(self, *args, **kwargs):
    auth = self.auth
    if not auth.get_user_by_session():
      self.redirect(self.uri_for('login'), abort=True)
    else:
      return handler(self, *args, **kwargs)

  return check_login

class BaseHandler(webapp2.RequestHandler):
  @webapp2.cached_property
  def auth(self):
    """Shortcut to access the auth instance as a property."""
    return auth.get_auth()

  @webapp2.cached_property
  def user_info(self):
    """Shortcut to access a subset of the user attributes that are stored
    in the session.

    The list of attributes to store in the session is specified in
      config['webapp2_extras.auth']['user_attributes'].
    :returns
      A dictionary with most user information
    """
    return self.auth.get_user_by_session()

  @webapp2.cached_property
  def user(self):
    """Shortcut to access the current logged in user.

    Unlike user_info, it fetches information from the persistence layer and
    returns an instance of the underlying model.

    :returns
      The instance of the user model associated to the logged in user.
    """
    u = self.user_info
    return self.user_model.get_by_id(u['user_id']) if u else None

  @webapp2.cached_property
  def user_model(self):
    """Returns the implementation of the user model.

    It is consistent with config['webapp2_extras.auth']['user_model'], if set.
    """    
    return self.auth.store.user_model

  @webapp2.cached_property
  def session(self):
      """Shortcut to access the current session."""
      return self.session_store.get_session(backend="datastore")

  def render_template(self, view_filename, params=None):
    if not params:
      params = {}
    user = self.user_info
    params['user'] = user
    path = os.path.join(os.path.dirname(__file__), 'html', view_filename)
    self.response.out.write(template.render(path, params))

  def display_message(self, message):
    """Utility function to display a template with a simple message."""
    params = {
      'message': message
    }
    self.render_template('message.html', params)

  # this is needed for webapp2 sessions to work
  def dispatch(self):
      # Get a session store for this request.
      self.session_store = sessions.get_store(request=self.request)

      try:
          # Dispatch the request.
          webapp2.RequestHandler.dispatch(self)
      finally:
          # Save all sessions.
          self.session_store.save_sessions(self.response)

class MainHandler(BaseHandler):
  @user_required
  def get(self):
    friend_list = FriendList.get_friend_list(self.user.auth_ids[0])
    if not friend_list:
      friend_count = 0
    else:
      friend_count = len(friend_list)

    token = channel.create_channel(self.user.auth_ids[0])
    params = {
      'friend_count': friend_count,
      'friend_list': friend_list,
      'token': token,
    }
    self.render_template('chat.html', params)

class SignupHandler(BaseHandler):
  def get(self):
    self.render_template('signup.html')

  def post(self):
    user_name = self.request.get('username')
    name = self.request.get('name')
    password = self.request.get('password')
    password1 = self.request.get('password1')

    if password != password1: # check that passwords match
      self.display_message('Passwords do not match')
      return 

    user_data = self.user_model.create_user(user_name,
      None,
      name=name,
      password_raw=password,
      verified=False)
    
    user = user_data[1]
    user_id = user.get_id()
    token = self.user_model.create_signup_token(user_id)
    self.redirect(self.uri_for('login'))

class LoginHandler(BaseHandler):
  def get(self):
    self._serve_page()

  def post(self):
    username = self.request.get('username')
    password = self.request.get('password')
    
    try:
      u = self.auth.get_user_by_password(username, password, remember=True,
        save_session=True)
      self.redirect(self.uri_for('home'))
    except (InvalidAuthIdError, InvalidPasswordError) as e:
      logging.info('Login failed for user %s because of %s', username, type(e))
      self._serve_page(True)

  def _serve_page(self, failed=False):
    username = self.request.get('username')
    params = {
      'username': username,
      'failed': failed
    }
    self.render_template('login.html', params)

class LogoutHandler(BaseHandler):
  def get(self):
    self.auth.unset_session()
    self.redirect(self.uri_for('login'))

class AddFriendHandler(BaseHandler):
  @user_required
  def get(self):
    self.render_template('add_friend.html')

  @user_required
  def post(self):
    friend_name = self.request.get('username')
    # doesn't make sense to search for yourself
    if friend_name != self.user.auth_ids[0]:
      user_info = User.query_user(friend_name)
      if user_info:
        if FriendList.add_friend(self.user.auth_ids[0], friend_name):
          self.redirect(self.uri_for('home'))
          return
    
    self.redirect(self.uri_for('add'))

class SendMessageHandler(BaseHandler):
  @user_required
  def post(self):
    receiver = self.request.get('to')
    msg = self.request.get('msg')
    self.dispatchMessage(receiver, msg)

  def dispatchMessage(self, receiver, msg):
    #print "sending message \"" + msg + "\" to " + "\"" + receiver + "\""
    newMessage = {
      'from': self.user.auth_ids[0],
      'msg': msg,
    }

    channel.send_message(receiver, json.dumps(newMessage))
    
config = {
  'webapp2_extras.auth': {
    'user_model': 'models.User',
    'user_attributes': ['name']
  },
  'webapp2_extras.sessions': {
    'secret_key': 'YOUR_SECRET_KEY'
  }
}

application = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name='home'),
    webapp2.Route('/signup', SignupHandler),
    webapp2.Route('/login', LoginHandler, name='login'),
    webapp2.Route('/logout', LogoutHandler, name='logout'),
    webapp2.Route('/add_friend', AddFriendHandler, name='add'),
    webapp2.Route('/send_message', SendMessageHandler, name='message')
], debug=True, config=config)

logging.getLogger().setLevel(logging.DEBUG)

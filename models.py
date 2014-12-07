import time
import webapp2_extras.appengine.auth.models
from google.appengine.ext import ndb
from google.appengine.ext import db
from webapp2_extras import security

class FriendList(ndb.Model):
  username = ndb.StringProperty()
  friends = ndb.StringProperty(repeated=True)

  @classmethod
  def query_friends(cls, user_name):
    return FriendList.query(FriendList.username == user_name).fetch()

  @classmethod
  def add_friend (cls, user_name, friend_name):
    #check to see if user exists
    query = cls.query_friends(user_name)
    if not query:
      print "No friend list information for " + user_name + ", Let's create it"
      query = FriendList(username = user_name, friends=[])
    elif friend_name in query[0].friends:
      print friend_name + " is already " + user_name + "'s friend"
      return False

    query[0].friends.append(friend_name)
    query[0].put()
    return True
  
  @classmethod
  def delete_friend(cls, user_name, friend_name):
    #check to see if user exists
    query = cls.query_friends(user_name)
    if not query:
      print user_name + " is not valid"
      return False

    if not (friend_name in query.friends):
      print friend_name + " is not " + user_name + "'s friend"
      return False

    query[0].friends.delete(friend_name)
    query[0].put()
    return True

  @classmethod
  def get_friend_list(cls, user_name):
    query = cls.query_friends(user_name)
    if not query:
      print user_name + " is not valid"

    return query[0].friends

class User(webapp2_extras.appengine.auth.models.User):
  def set_password(self, raw_password):
    """Sets the password for the current user

    :param raw_password:
        The raw password which will be hashed and stored
    """
    self.password = security.generate_password_hash(raw_password, length=12)
  
  @classmethod
  def get_by_auth_token(cls, user_id, token, subject='auth'):
    """Returns a user object based on a user ID and token.

    :param user_id:
        The user_id of the requesting user.
    :param token:
        The token string to be verified.
    :returns:
        A tuple ``(User, timestamp)``, with a user object and
        the token timestamp, or ``(None, None)`` if both were not found.
    """
    token_key = cls.token_model.get_key(user_id, subject, token)
    user_key = ndb.Key(cls, user_id)
    # Use get_multi() to save a RPC call.
    valid_token, user = ndb.get_multi([token_key, user_key])
    if valid_token and user:
        timestamp = int(time.mktime(valid_token.created.timetuple()))
        return user, timestamp

    return None, None

  @classmethod
  def query_user(cls, user_name):
    return User.query(ndb.GenericProperty('auth_ids') == user_name).fetch()
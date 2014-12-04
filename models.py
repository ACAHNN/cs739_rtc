import time
import webapp2_extras.appengine.auth.models

from google.appengine.ext import ndb
from webapp2_extras.appengine.auth.models import UserToken

try:
    from ndb import model
except ImportError: # pragma: no cover
    from google.appengine.ext.ndb import model

from webapp2_extras import security


#outerclass for user to hold the built in user structrue and our friendslist  
class OuterUser(model.Expando):
  
  m_userName = model.StringProperty
  m_key = model.IntegerProperty #key to user object created by signup process. Contains password, name, authid
  
  m_friends = model.StringProperty(repeated = True) #list of friends authIDs
  
  def add_friend (self, friendName):
    #returns true if friend could be added
    #friendname is the authid of the friend.
    
    #check to see if user exists
    query = OuterUser.query(ndb.GenericProperty("m_userName") == friendName).fetch()
    if not query:
        return False, "no such user"
    
    self.m_friends.append(friendName)
    self.put()
  
  

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
  def create_user(cls, auth_id, unique_properties=None, **user_values):
    """Creates a new user.

    :param auth_id:
        A string that is unique to the user. Users may have multiple
        auth ids. Example auth ids:

        - own:username
        - own:email@example.com
        - google:username
        - yahoo:username

        The value of `auth_id` must be unique.
    :param unique_properties:
        Sequence of extra property names that must be unique.
    :param user_values:
        Keyword arguments to create a new user entity. Since the model is
        an ``Expando``, any provided custom properties will be saved.
        To hash a plain password, pass a keyword ``password_raw``.
    :returns:
        A tuple (boolean, info). The boolean indicates if the user
        was created. If creation succeeds, ``info`` is the user entity;
        otherwise it is a list of duplicated unique properties that
        caused creation to fail.
    """
    assert user_values.get('password') is None, \
        'Use password_raw instead of password to create new users.'

    assert not isinstance(auth_id, list), \
        'Creating a user with multiple auth_ids is not allowed, ' \
        'please provide a single auth_id.'

    if 'password_raw' in user_values:
        user_values['password'] = security.generate_password_hash(
            user_values.pop('password_raw'), length=12)
    user_values['auth_ids'] = [auth_id]
    user = cls(m_userName=auth_id, **user_values)  # added user_name
    # Set up unique properties.
    uniques = [('%s.auth_id:%s' % (cls.__name__, auth_id), 'auth_id')]
    if unique_properties:
        for name in unique_properties:
            key = '%s.%s:%s' % (cls.__name__, name, user_values[name])
            uniques.append((key, name))

    ok, existing = cls.unique_model.create_multi(k for k, v in uniques)
    
    
    if ok:
        ndb_key = user.put() #added
        outeruser = OuterUser(m_userName = auth_id, m_key = ndb_key) #added
        outeruser.put() #added
        return True, user, ndb_key #added
    else:
        properties = [v for k, v in uniques if k in existing]
        return False, properties

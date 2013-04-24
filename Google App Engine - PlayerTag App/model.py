from google.appengine.ext import ndb
##==============================================================================##
##    Model.py Contains Datastore Entities                                      ##
##==============================================================================##
##      Author:         C00117798 - Olawale Egbeyemi                            ##
##      Date:           11/12/2010                                              ##
##      Last Modified:  13/01/2013                                              ##
##      Description:                                                            ##
##      Python Version:  2.7                                                    ##
##==============================================================================##
##==============================================================================##
   
#Player Tag Entity
class PlayerTag(ndb.Model):
    tag = ndb.StringProperty()
    google_id = ndb.UserProperty()
    password = ndb.StringProperty()
    confirm = ndb.BooleanProperty()
    friends = ndb.KeyProperty(repeated=True)
    activationToken = ndb.StringProperty()

class Team(ndb.Model):
    administrator = ndb.KeyProperty()
    teamName = ndb.StringProperty()
    members = ndb.KeyProperty(repeated=True)
    
class FriendsRequest(ndb.Model):
    fromTag = ndb.KeyProperty()
    toTag = ndb.KeyProperty()
    confirmation = ndb.StringProperty()

#Email Archive entity
class EmailArchive(ndb.Model):
    from_ = ndb.StringProperty()
    subject = ndb.StringProperty()
    content = ndb.TextProperty()

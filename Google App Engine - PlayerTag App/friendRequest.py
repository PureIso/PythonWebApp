import webapp2
import jinja2 
import os
import model
import functions

from google.appengine.ext import ndb

##==============================================================================##
##    FriendRequest.py Request a player tag to be your friend                   ##
##==============================================================================##
##      Author:         C00117798 - Olawale Egbeyemi                            ##
##      Date:           11/12/2010                                              ##
##      Last Modified:  29/12/2012                                              ##
##      Description:                                                            ##
##      Python Version:  2.7                                                    ##
##==============================================================================##
##==============================================================================##

#Global Variable
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class FriendRequestHandler(webapp2.RequestHandler):    #Web Page Index Handler Class  
    def get(self):
        the_CurrentUser = self.request.get('currentUser')
        query = model.PlayerTag.query(str(model.PlayerTag.tag) == the_CurrentUser,
                                      model.PlayerTag.confirm == True)
        
        if(query.count() > 0):
            for player in query:
                the_CurrentUser = player.key.urlsafe()                      
                the_CurrentUser = ndb.Key(urlsafe=the_CurrentUser).get()
                
                items = []
                #Query for all the request for the current user
                query = model.FriendsRequest.query(model.FriendsRequest.toTag == the_CurrentUser.key,
                                                   model.FriendsRequest.confirmation == "Awaiting",
                                                   model.FriendsRequest.fromTag != the_CurrentUser.key)
                if(query > 0):
                    #each request
                    for item in query:  #query = FriendRequest
                        #Query for any player with the key
                        playerQuery = model.PlayerTag.query(model.PlayerTag.key == item.fromTag)
                        if(playerQuery > 0):                    #if we have a value
                            for innerItem in playerQuery:       #We now have the PlayerTag'
                                items.append(innerItem)         #Append the PlayerTag to the items List
                                
                template = jinja_environment.get_template('templates/friendRequest.html')
                html = template.render({'query': items,
                                        'the_title': 'Friend Request',
                                        'PlayerTags': model.PlayerTag.query(model.PlayerTag.confirm == True,
                                                                            model.PlayerTag.tag != the_CurrentUser.tag),
                                        'playerTagHeader': the_CurrentUser.tag,})
        else:
            template = jinja_environment.get_template('templates/friendRequest.html')
            html = template.render({'the_title': 'Friend Request',
                                    'PlayerTags': model.PlayerTag.query(model.PlayerTag.confirm == True),
                                    'playerTagHeader': the_CurrentUser.tag,})
        self.response.out.write(html)
   
    def post(self):
        to_Player = self.request.get('tags')                            #Get the key of the player you are sending invites to
        
        playerTagKey = functions.Worker.PlayerTagStringToPlayerKey(self.request.get('currentUser'))
        friends = functions.Worker.GetFriendsList(playerTagKey)
                  
        try:
            new_Request = model.FriendsRequest()
            to_Player = ndb.Key(urlsafe=to_Player).get()                    
            
            new_Request.fromTag = playerTagKey.key
            new_Request.toTag = to_Player.key
            
            new_Request.confirmation = 'Awaiting'
            #Duplicates
            queryNew = model.FriendsRequest.query(ndb.OR(
                                                         ndb.AND(model.FriendsRequest.fromTag == playerTagKey.key, 
                                                                 model.FriendsRequest.toTag == to_Player.key),
                                                         ndb.AND(model.FriendsRequest.fromTag == to_Player.key, 
                                                                 model.FriendsRequest.toTag == playerTagKey.key)
                                                         ))
            #If no Duplicates what so ever
            if(queryNew.count() == 0):
                new_Request.put()
                template = jinja_environment.get_template('templates/dash.html')
                html = template.render({'playerTagHeader': playerTagKey.tag,
                                        'the_title': 'Dashboard',
                                        'friends' : friends})
            else:
                #We have Decline or Awaiting
                queryDub = model.FriendsRequest.query(ndb.OR(
                                                             ndb.AND(model.FriendsRequest.fromTag == playerTagKey.key, 
                                                                     model.FriendsRequest.toTag == to_Player.key),
                                                             ndb.AND(model.FriendsRequest.fromTag == to_Player.key, 
                                                                     model.FriendsRequest.toTag == playerTagKey.key)
                                                             ),
                                                      ndb.AND(model.FriendsRequest.confirmation == 'Decline')
                                                      )
                #You were declined
                if(queryDub.count() > 0):
                    #Give another chance
                    for item in queryDub:
                        item.confirmation = 'Awaiting'
                        item.put();
                            
                        template = jinja_environment.get_template('templates/dash.html')
                        html = template.render({'playerTagHeader': playerTagKey.tag,
                                            'the_title': 'Dashboard',
                                            'friends' : friends})
                        """
                        #No more chances
                        template = jinja_environment.get_template('templates/friendRequest.html')
                        html = template.render({'playerTagHeader': the_CurrentUser.tag,
                                            'the_title': 'Friend Request',
                                            'errorMatch': 'Request was Declined by the user',
                                            'PlayerTags': model.PlayerTag.query(model.PlayerTag.confirm == True,
                                                                            model.PlayerTag.tag != the_CurrentUser.tag),})
                    """
                #Still Awaiting
                else:
                    template = jinja_environment.get_template('templates/friendRequest.html')
                    html = template.render({'playerTagHeader': playerTagKey.tag,
                                            'the_title': 'Friend Request',
                                            'errorMatch': 'User already sent a friends request',
                                            'PlayerTags': model.PlayerTag.query(model.PlayerTag.confirm == True,
                                                                                model.PlayerTag.tag != playerTagKey.tag),})
        except TypeError:
            new_Request.fromTag = None
            new_Request.toTag = None
            template = jinja_environment.get_template('templates/friendRequest.html')
            html = template.render({'playerTagHeader': playerTagKey.tag,
                                    'the_title': 'Friend Request',
                                    'errorMatch': 'Unknown Error',
                                    'PlayerTags': model.PlayerTag.query(model.PlayerTag.confirm == True,
                                                                            model.PlayerTag.tag != playerTagKey.tag),})

        #return the html page
        self.response.out.write(html)        

app = webapp2.WSGIApplication([ ('/friendRequest', FriendRequestHandler),], debug=True)
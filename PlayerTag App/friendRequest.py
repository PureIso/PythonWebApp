import cherrypy
import jinja2
import os
import sys
import functions
from model import PlayerTag, FriendsRequest

##==============================================================================##
##    FriendRequest.py Request a player tag to be your friend                   ##
##==============================================================================##
##      Author:         C00117798 - Olawale Egbeyemi                            ##
##      Date:           29/03/2013                                              ##
##      Last Modified:  13/04/2013                                              ##
##      Description:                                                            ##
##      Python Version:  2.7                                                    ##
##==============================================================================##
##==============================================================================##

#Global Variable
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class FriendRequest(object):
    def POST(self,playerTag,selectedTag):         
        try:
            connection = functions.Worker()
            playerTagObject = PlayerTag()                                  
            playerTagObject.SetPlayerTag(playerTag)
            
            notFriendsWith = connection.NonFriendsList(playerTagObject)
            
            new_Request = FriendsRequest()
            new_Request.SetFromTag(playerTag)
            new_Request.SetToTag(selectedTag)
            new_Request.SetConfirmation('Awaiting')
            #Duplicates
            queryNew = connection.FindFriendRequestDuplicate(new_Request)
        except:
            new_Request.fromTag = None
            new_Request.toTag = None
            template = jinja_environment.get_template('templates/friendRequest.html')
            return template.render({'playerTagHeader': playerTagObject.GetPlayerTag(),
                                    'the_title': 'Friend Request',
                                    'errorMatch': ("Unexpected error:", sys.exc_info()[1]),
                                    'PlayerTags': notFriendsWith,})
            
        #If no Duplicates what so ever
        if(queryNew.__len__() == 0):
            connection.InsertFriendRequest(new_Request)
            raise cherrypy.HTTPRedirect("/dash/", 302)
        else:
            #We have Decline or Awaiting
            queryDub = connection.FindFriendRequest(new_Request)
            #You were declined
            if(queryDub.__len__() > 0):
                #Give another chance
                for item in queryDub:
                    if(item['Confirmation'] == 'Decline'):
                        item.SetConfirmation('Awaiting')
                        connection.InsertFriendRequest(item)
                        raise cherrypy.HTTPRedirect("/dash/", 302)
                    #Still Awaiting
                    else:
                        template = jinja_environment.get_template('templates/friendRequest.html')
                        return template.render({'playerTagHeader': playerTagObject.GetPlayerTag(),
                                                'the_title': 'Friend Request',
                                                'errorMatch': 'User already sent a friends request',
                                                'PlayerTags': notFriendsWith,})
        
    
    def GET(self,playerName):
        try:
            connection = functions.Worker()
            playerTagObject = PlayerTag()                                  
            playerTagObject.SetPlayerTag(playerName)
            
            notFriendsWith = connection.NonFriendsList(playerTagObject)
            
        except TypeError:
            template = jinja_environment.get_template('templates/friendRequest.html')
            return template.render({'playerTagHeader': playerTagObject.GetPlayerTag(),
                                    'the_title': 'Friend Request',
                                    'errorMatch': ("Unexpected error:", sys.exc_info()[1]),
                                    'PlayerTags': notFriendsWith,})
            
        if (notFriendsWith.__len__() == 0):
            raise cherrypy.HTTPRedirect("/dash/", 302)
        else:        
            template = jinja_environment.get_template('templates/friendRequest.html')
            return template.render({'the_title': 'Friend Request',
                                    'PlayerTags': notFriendsWith,
                                    'playerTagHeader': playerTagObject.GetPlayerTag(),})
                
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['get', 'post'])
    def index(self,playerName=None,selectedTag=None):
        playerName = cherrypy.session.get("PlayerTag")
        if(cherrypy.request.method == 'GET'):
            return self.GET(playerName)
        else:
            return self.POST(playerName, selectedTag)
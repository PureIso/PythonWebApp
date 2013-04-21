import cherrypy
import jinja2
import os
import sys
import functions
from model import PlayerTag

##==============================================================================##
##    PendingRequest.py Accept of Decline Pending Friend Request                ##
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

class PendingRequest(object):
    
    def POST(self,playerName, requestPending, button):
        try:
            connection = functions.Worker()
            playerTagObject = PlayerTag()                                  
            playerTagObject.SetPlayerTag(playerName)
            
            selectedTagObject = PlayerTag()  
            selectedTagObject = PlayerTag(requestPending)
            
            playerTagObject = connection.FindPlayerTagNoPass(playerTagObject)
            selectedTagObject = connection.FindPlayerTagNoPass(selectedTagObject)
            
            #Get friend request object
            friendRequestObject = connection.GetRequestPendingForFrom(selectedTagObject, playerTagObject)
        except:
            playerTagObject = PlayerTag()                                  
            playerTagObject.SetPlayerTag(playerName)
            requestPendingList = connection.GetRequestPendingFor(playerTagObject)
            template = jinja_environment.get_template('templates/pendingRequest.html')
            return template.render({'FriendRequests': requestPendingList,
                                    'the_title': 'Pending Request',
                                    'errorMatch': ("Unexpected error:", sys.exc_info()[1]),
                                    'playerTagHeader': playerTagObject.GetPlayerTag(),})
            
        if(button == 'Accept'):
            if(playerTagObject['Friends'].__contains__(selectedTagObject['PlayerTag']) or
               selectedTagObject['Friends'].__contains__(playerTagObject['PlayerTag'])):return
            
            for request in friendRequestObject:
                request['Confirmation'] = "Accept"
                connection.UpdateFriendRequest(request)
            
            playerTagObject['Friends'].append(selectedTagObject['PlayerTag'])
            selectedTagObject['Friends'].append(playerTagObject['PlayerTag'])
            
            connection.UpdatePlayerTag(playerTagObject)
            connection.UpdatePlayerTag(selectedTagObject)
        else:
            for request in friendRequestObject:
                request['Confirmation'] = "Decline"
                connection.UpdateFriendRequest(request)
        
        
        playerTagObject = PlayerTag()                                  
        playerTagObject.SetPlayerTag(playerName)
        
        raise cherrypy.HTTPRedirect("/dash/", 302)
        

    def GET(self,playerTag):
        try:
            connection = functions.Worker()
            playerTagObject = PlayerTag()                                  
            playerTagObject.SetPlayerTag(playerTag)
            requestPendingList =connection.GetRequestPendingFor(playerTagObject)
        except TypeError:
            template = jinja_environment.get_template('templates/pendingRequest.html')
            return template.render({'FriendRequests': requestPendingList,
                                    'the_title': 'Pending Request',
                                    'errorMatch': ("Unexpected error:", sys.exc_info()[1]),
                                    'playerTagHeader': playerTagObject.GetPlayerTag(),})
            
        if(requestPendingList.__len__() == 0):
            raise cherrypy.HTTPRedirect("/dash/", 302)
        else:
            template = jinja_environment.get_template('templates/pendingRequest.html')
            return template.render({'FriendRequests': requestPendingList,
                                    'the_title': 'Pending Request',
                                    'playerTagHeader': playerTagObject.GetPlayerTag(),})
        
            
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['get', 'post'])
    def index(self,requestPending=None, button=None,playerName=None):
        playerName = cherrypy.session.get("PlayerTag")
        if(cherrypy.request.method == 'GET'):
            return self.GET(playerName)
        else:
            return self.POST(playerName, requestPending, button)


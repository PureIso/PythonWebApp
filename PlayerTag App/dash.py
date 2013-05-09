import cherrypy
import jinja2
import os
import sys
import functions
from model import PlayerTag

##==============================================================================##
##    Dash.py Displays the Main Home Screen                                     ##
##==============================================================================##
##      Author:         C00117798 - Olawale Egbeyemi                            ##
##      Date:           29/03/2013                                              ##
##      Last Modified:  13/04/2013                                              ##
##      Description:                                                            ##
##      Python Version:  2.7                                                    ##
##      NB:                                                                     ##
##==============================================================================##
##==============================================================================##

#Global Variable
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Dash(object):
    def POST(self,playerName, page):
        try:
            connection = functions.Worker()
            playerTagObject = PlayerTag()                                  
            playerTagObject.SetPlayerTag(playerName)
            friends = connection.GetFriends(playerTagObject)
            team = connection.GetTeams(playerTagObject)
        except:
            template = jinja_environment.get_template('templates/dash.html')   
            return template.render({'playerTagHeader': playerTagObject.GetPlayerTag(),
                                    'the_title': 'Dashboard',
                                    'friends' : friends,
                                    'teams': team,
                                    'errorMatch': ("Unexpected error:", sys.exc_info()[1])})        
        #If friend request option selected
        if(page == 'friendRequest'):
            notFriendsWith = connection.NonFriendsList(playerTagObject)
            if (notFriendsWith.__len__() == 0):
                template = jinja_environment.get_template('templates/dash.html')
                return template.render({'the_title': 'Dashboard',
                                        'errorMatch': 'You are friends with everyone or Your Request/s are Pending !',
                                        'playerTagHeader' : playerTagObject.GetPlayerTag(),
                                        'teams' : team,
                                        'friends': friends})
            else:
                raise cherrypy.HTTPRedirect("/friendRequest/", 302)     
                
        #If pending Request option selected    
        elif (page == 'pendingRequest'):
            requestPendingList =connection.GetRequestPendingFor(playerTagObject)

            if(requestPendingList.__len__() == 0):
                template = jinja_environment.get_template('templates/dash.html')
                return template.render({'the_title': 'Dashboard',
                                        'errorMatch': 'No Request Pending',
                                        'playerTagHeader' : playerTagObject.GetPlayerTag(),
                                        'teams' : team,
                                        'friends': friends})
            else:
                raise cherrypy.HTTPRedirect("/pendingRequest/", 302)
        
        #If Team set up is selected
        else:
            raise cherrypy.HTTPRedirect("/teams/", 302)
    
    def GET(self,playerName): 
        connection = functions.Worker()
        playerTagObject = PlayerTag()                                  
        playerTagObject.SetPlayerTag(playerName)
        friends = connection.GetFriends(playerTagObject)
        team = connection.GetTeams(playerTagObject)
                           
        template = jinja_environment.get_template('templates/dash.html')   
        return template.render({'playerTagHeader': playerTagObject.GetPlayerTag(),
                                'the_title': 'Dashboard',
                                'friends' : friends,
                                'teams': team})
        
    @cherrypy.expose
    def index(self,playerName=None, page=None):
        playerName = cherrypy.session.get("PlayerTag")
        if(cherrypy.request.method == 'GET'):
            return self.GET(playerName)
        else:
            return self.POST(playerName, page)
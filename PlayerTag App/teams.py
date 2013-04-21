import cherrypy
import jinja2
import os
import sys
import functions
from model import PlayerTag, Team

##==============================================================================##
##    Teams.py  Allows for the ability to setup a team                          ##
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

class TeamRequest(object):
        
    def POST(self,playerName, page, selectedTeam):
        try:
            connection = functions.Worker()
            playerTagObject = PlayerTag()                                  
            playerTagObject.SetPlayerTag(playerName)
            
            team = connection.GetTeams(playerTagObject)  
            
            selectedTeamObject = Team()                                  
            selectedTeamObject.SetTeamName(selectedTeam)
        except:
            template = jinja_environment.get_template('templates/teams.html')
            return template.render({'playerTagHeader': playerTagObject.GetPlayerTag(),
                                    'the_title': 'Team Menu',
                                    'teams':team,
                                    'errorMatch': ("Unexpected error:", sys.exc_info()[1])
                                    })
                            
        #If friend request option selected
        if(page == 'createnewteam'):   
            raise cherrypy.HTTPRedirect("/createnewteam/", 302)  
        
        #If pending Request option selected    
        elif (page == 'joinateam'):
            teamNames = connection.GetAllTeams()
            for item in team:
                if(teamNames.__contains__(item)):
                    teamNames.remove(item)
            
            if(teamNames.__len__() > 0):
                raise cherrypy.HTTPRedirect("/joinateam/", 302)
            else:
                template = jinja_environment.get_template('templates/teams.html')
                return template.render({'the_title': 'Join A Team',
                                        'errorMatch' : 'No Teams Available!',
                                        'teams':team,
                                        'playerTagHeader': playerTagObject.GetPlayerTag(),})
        #If Team set up is selected
        else:
            teamDB = connection.FindTeam(selectedTeamObject)
            if(teamDB == ""):
                template = jinja_environment.get_template('templates/teams.html')
                return template.render({'the_title': 'Manage A Team',
                                        'errorMatch' : 'No Teams Available!',
                                        'teams':team,
                                        'playerTagHeader': playerTagObject.GetPlayerTag(),})
            else:
                cherrypy.session['selectedTeam'] = selectedTeam
                raise cherrypy.HTTPRedirect("/manageateam/", 302)
         
    
    def GET(self,playerName):
        connection = functions.Worker()
        playerTagObject = PlayerTag()                                  
        playerTagObject.SetPlayerTag(playerName)
        team = connection.GetTeams(playerTagObject)        
        template = jinja_environment.get_template('templates/teams.html')   
        return template.render({'playerTagHeader': playerName,
                                'the_title': 'Team Menu',
                                'teams':team})
        
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['get', 'post'])
    def index(self,playerName=None, page=None, selectedTeam=None):
        playerName = cherrypy.session.get("PlayerTag")
        if(cherrypy.request.method == 'GET'):
            return self.GET(playerName)
        else:
            return self.POST(playerName, page, selectedTeam)
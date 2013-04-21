import cherrypy
import jinja2
import os
import sys
import functions
from model import PlayerTag, Team

##==============================================================================##
##    JoinATeam.py Join a Team                                                  ##
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

class JoinATeam(object):    #Web Page Index Handler Class
        
    def POST(self,playerName, selectedTeam):
        try:
            connection = functions.Worker()
            playerTagObject = PlayerTag()                                  
            playerTagObject.SetPlayerTag(playerName)
                
            selectedTeamObject = Team()                                  
            selectedTeamObject.SetTeamName(selectedTeam)
            
            teamNames = connection.GetAllTeams()
            team = connection.GetTeams(playerTagObject)
            for item in team:
                if(teamNames.__contains__(item)):
                    teamNames.remove(item)
        except:
            template = jinja_environment.get_template('templates/joinateam.html')
            return template.render({'playerTagHeader': playerTagObject.GetPlayerTag(),
                                    'errorMatch': ("Unexpected error:", sys.exc_info()[1]),
                                    'teams' : teamNames})
                       
        #Check if this user is part of this current team
        teamMember = connection.GetTeams(playerTagObject)
                        
        if(teamMember.__contains__(selectedTeam)):
            template = jinja_environment.get_template('templates/joinateam.html')
            return template.render({'the_title': 'Join A Team.',
                                    'playerTagHeader': playerTagObject.GetPlayerTag(),
                                    'errorMatch': 'Player Tag is already a member of this Team!',
                                    'teams' : teamNames})
        else:
            teamDB = connection.FindTeam(selectedTeamObject)
            teamDB['Members'].append(playerName)
            connection.UpdateTeam(teamDB)
            
            playerDB = connection.FindPlayerTagNoPass(playerTagObject)
            playerDB['Teams'].append(teamDB['TeamName'])
            connection.UpdatePlayerTag(playerDB)
            raise cherrypy.HTTPRedirect("/dash/", 302)  
            
    def GET(self,playerName):
        try:
            connection = functions.Worker()
            playerTagObject = PlayerTag()                                  
            playerTagObject.SetPlayerTag(playerName)
            
            teamNames = connection.GetAllTeams()
            team = connection.GetTeams(playerTagObject)
            for item in team:
                if(teamNames.__contains__(item)):
                    teamNames.remove(item)
        except:
            template = jinja_environment.get_template('templates/joinateam.html')
            return template.render({'playerTagHeader': playerTagObject.GetPlayerTag(),
                                    'errorMatch': ("Unexpected error:", sys.exc_info()[1]),
                                    'teams' : teamNames})
                                
        template = jinja_environment.get_template('templates/joinateam.html')
        return template.render({'the_title': 'Join A Team.',
                                'playerTagHeader' : playerName,
                                'teams' : teamNames})
        
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['get', 'post'])
    def index(self,playerName=None, selectedTeam=None):
        playerName = cherrypy.session.get("PlayerTag")
        if(cherrypy.request.method == 'GET'):
            return self.GET(playerName)
        else:
            return self.POST(playerName, selectedTeam)
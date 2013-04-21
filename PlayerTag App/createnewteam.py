import cherrypy
import jinja2
import os
import sys
import functions
from model import PlayerTag, Team

##==============================================================================##
##    CreateNewTeam.py Create a new Team                                        ##
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

class CreateNewTeam(object):    #Web Page Index Handler Class  
    
    def POST(self,playerName, teamName, teamNameConfirm):
        try:
            connection = functions.Worker()
            playerTagObject = PlayerTag()                                  
            playerTagObject.SetPlayerTag(playerName)
                
            teamObject = Team()                                  
            teamObject.SetTeamName(teamName)
        except:
            template = jinja_environment.get_template('templates/createnewteam.html')
            return template.render({'playerTagHeader': playerTagObject.GetPlayerTag(),
                                    'errorMatch': ("Unexpected error:", sys.exc_info()[1])})
            
        if(teamName != teamNameConfirm):
            template = jinja_environment.get_template('templates/createnewteam.html')
            return template.render({'playerTagHeader': playerTagObject.GetPlayerTag(),
                                    'errorTeam': 'Team Name does not match!'})
            
        elif(teamName == ""):
            template = jinja_environment.get_template('templates/createnewteam.html')
            return template.render({'playerTagHeader': playerTagObject.GetPlayerTag(),
                                    'errorTeam': 'Empty Name not accepted!'})
            
        else:
            #Find Duplicates
            teams = connection.FindTeam(teamObject)
            if(str(teams) != 'None'):
                template = jinja_environment.get_template('templates/createnewteam.html')
                return template.render({'playerTagHeader': playerTagObject.GetPlayerTag(),
                                        'errorTeam': 'This team already exist!'})
            else:
                teamObject.SetAdministrator(playerTagObject.GetPlayerTag())
                teamObject.SetMembers(playerTagObject.GetPlayerTag())
                connection.InsertTeam(teamObject)
                
                playerDB = connection.FindPlayerTagNoPass(playerTagObject)
                playerDB['Teams'].append(teamObject.GetTeamName())
                connection.UpdatePlayerTag(playerDB)

                raise cherrypy.HTTPRedirect("/dash/", 302)  
                
    def GET(self,playerName):                
        template = jinja_environment.get_template('templates/createnewteam.html')   
        return template.render({'playerTagHeader': playerName,
                                'the_title': 'Create a New Team'})
        
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['get', 'post'])
    def index(self,playerName=None, teamName=None, teamNameConfirm=None):
        playerName = cherrypy.session.get("PlayerTag")
        if(cherrypy.request.method == 'GET'):
            return self.GET(playerName)
        else:
            return self.POST(playerName, teamName, teamNameConfirm)
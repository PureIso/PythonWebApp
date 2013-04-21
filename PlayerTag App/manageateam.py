import cherrypy
import jinja2
import os
import sys
import functions
from model import PlayerTag, Team

##==============================================================================##
##    ManageATeam.py Manage A Team                                              ##
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

class ManageATeam(object):    #Web Page Index Handler Class
        
    def POST(self,playerName, currentTeam, selectedMember):
        try:
            connection = functions.Worker()
            playerTagObject = PlayerTag()                                  
            playerTagObject.SetPlayerTag(playerName)
            
            currentTeamObject = Team()                                  
            currentTeamObject.SetTeamName(currentTeam)
    
            selectedMemberObject = PlayerTag()                                  
            selectedMemberObject.SetPlayerTag(selectedMember)
            
            teamDB = connection.FindTeam(currentTeamObject)
            members = []
            for member in teamDB['Members']:
                if(members.__contains__(member)):continue
                else: members.append(member)
        except:
            template = jinja_environment.get_template('templates/manageateam.html')
            return template.render({'the_title': 'Manage A Team.',
                                    'playerTagHeader': playerName,
                                    'errorMatch': ("Unexpected error:", sys.exc_info()[1]),
                                    'team' : currentTeam,
                                    'members' : members})
         
        if(teamDB['Administrator'] != playerName):
            template = jinja_environment.get_template('templates/manageateam.html')
            return template.render({'the_title': 'Manage A Team.',
                                    'playerTagHeader': playerName,
                                    'errorMatch': 'Administrators privilege required in order to remove members.',
                                    'team' : currentTeam,
                                    'members' : members})
        else:   
            if(teamDB['Administrator'] == selectedMember):
                template = jinja_environment.get_template('templates/manageateam.html')
                return template.render({'the_title': 'Manage A Team.',
                                        'playerTagHeader': playerName,
                                        'errorMatch': 'Administrators cannot be removed. Delete the Team instead!',
                                        'team' : currentTeam,
                                        'members' : members})
            else:
                t = [] 
                t = teamDB['Members']
                for item in t:
                    if(item.__contains__(selectedMember)):
                        #Get the member
                        t.remove(item)
                        
                        playerTagObject = PlayerTag()                                  
                        playerTagObject.SetPlayerTag(str(item))
                        playerDB = connection.FindPlayerTagNoPass(playerTagObject)
                        playerDB['Teams'].remove(teamDB['TeamName'])
                        connection.UpdatePlayerTag(playerDB)
                        
                teamDB['Members'] = t
                connection.UpdateTeam(teamDB)
                raise cherrypy.HTTPRedirect("/dash/", 302)   
            
    def GET(self,playerName,currentTeam):
        try:
            connection = functions.Worker()
            currentTeamObject = Team()                                  
            currentTeamObject.SetTeamName(currentTeam)
            teamDB = connection.FindTeam(currentTeamObject)
            members = []
            for member in teamDB['Members']:
                if(members.__contains__(member)):continue
                else: members.append(member)

        except:
            template = jinja_environment.get_template('templates/manageateam.html')
            return template.render({'the_title': 'Manage A Team.',
                                    'playerTagHeader': playerName,
                                    'errorMatch': ("Unexpected error:", sys.exc_info()[1]),
                                    'team' : currentTeam,
                                    'members' : members})
                                       
        template = jinja_environment.get_template('templates/manageateam.html')
        return template.render({'the_title': 'Manage A Team.',
                                'playerTagHeader' : playerName,
                                'team' : currentTeam,
                                'members' : members})
        
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['get', 'post'])
    def index(self,playerName=None, selectedTeam=None, selectedMember=None):
        playerName = cherrypy.session.get("PlayerTag")
        selectedTeam = cherrypy.session.get("selectedTeam")
        
        if(cherrypy.request.method == 'GET'):
            return self.GET(playerName, selectedTeam)
        else:
            return self.POST(playerName, selectedTeam, selectedMember)
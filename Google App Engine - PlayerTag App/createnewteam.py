import webapp2
import jinja2 
import os
import model
import functions

##==============================================================================##
##    CreateNewTeam.py Creates a new Team                                       ##
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

class CreateNewTeamHandler(webapp2.RequestHandler):    #Web Page Index Handler Class  
    
    def post(self):
        template = jinja_environment.get_template('templates/teams.html')
        teamStringName = self.request.get('teamName')
        teamStringNameConfirm = self.request.get('teamNameConfirm')
        playerTagKey = functions.Worker.PlayerTagStringToPlayerKey(self.request.get('currentUser'))
        team = functions.Worker.GetPlayerTagTeamList(playerTagKey)
        
        if(teamStringName != teamStringNameConfirm):
            html = template.render({'playerTagHeader': playerTagKey.tag,
                                    'errorTeam': 'Team Name does not match!'})
        else:
            #Find Duplicates
            query = model.Team.query(model.Team.teamName == teamStringName)
            if(query.count() > 0):
                html = template.render({'playerTagHeader': playerTagKey.tag,
                                        'errorTeam': 'This team already exist!'})
            else:
                try:
                    newTeam = model.Team()
                    newTeam.administrator = playerTagKey.key
                    newTeam.teamName = teamStringName
                    newTeam.members.append(playerTagKey.key)
                    newTeam.put()
                    
                    team = functions.Worker.GetPlayerTagTeamList(playerTagKey)
                    friends = functions.Worker.GetFriendsList(playerTagKey)
                    template = jinja_environment.get_template('templates/dash.html')
                    html = template.render({'playerTagHeader': playerTagKey.tag,
                                            'teams' : team,
                                            'the_title': 'Dashboard',
                                            'friends' : friends})
                except:
                    html = template.render({'playerTagHeader': playerTagKey.tag,
                                            'errorMatch': 'An exception error occurred! '})

        #return the html page
        self.response.out.write(html)        

app = webapp2.WSGIApplication([ ('/createnewteam', CreateNewTeamHandler),], debug=True)
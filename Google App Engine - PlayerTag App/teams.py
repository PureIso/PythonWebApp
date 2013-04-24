import webapp2
import jinja2 
import os
import functions
import model

from google.appengine.ext import ndb
##==============================================================================##
##    Team.py Manages the team options                                          ##
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

class TeamRequestHandler(webapp2.RequestHandler):    #Web Page Index Handler Class
        
    def post(self):
        the_Page = self.request.get('page')
        playerTagKey = functions.Worker.PlayerTagStringToPlayerKey(self.request.get('currentUser'))
                       
        #If friend request option selected
        if(the_Page == 'createnewteam'):     
            template = jinja_environment.get_template('templates/createnewteam.html')
            html = template.render({'the_title': 'Create a new team.',
                                    'playerTagHeader': playerTagKey.tag,})
        
        #If pending Request option selected    
        elif (the_Page == 'joinateam'):
            teams = model.Team.query()
            if(teams.count() > 0):
                
                template = jinja_environment.get_template('templates/joinateam.html')
                html = template.render({'the_title': 'Join A Team.',
                                        'playerTagHeader' : playerTagKey.tag,
                                        'teams' : teams})
            else:
                template = jinja_environment.get_template('templates/teams.html')
                html = template.render({'the_title': 'Pending Request',
                                        'errorMatch' : 'No Teams Available!',
                                        'playerTagHeader': playerTagKey.tag,})
        #If Team set up is selected
        else:
            try:
                teamKey = ndb.Key(urlsafe=self.request.get('selectedTeam')).get()
            except:
                teamKey = ""
            
            if(teamKey == ""):
                template = jinja_environment.get_template('templates/teams.html')
                html = template.render({'the_title': 'Pending Request',
                                        'errorMatch' : 'No Teams Available!',
                                        'playerTagHeader': playerTagKey.tag,})
            else:
                members = functions.Worker.GetTeamMembersList(teamKey)
                memberPlayerTag = []
                for member in members:
                    member = functions.Worker.PlayerTagStringToPlayerKey(member)
                    memberPlayerTag.append(member)
                
                template = jinja_environment.get_template('templates/manageateam.html')
                html = template.render({'playerTagHeader': playerTagKey.tag,
                                        'the_title': 'Manage A Team',
                                        'team' : teamKey.teamName,
                                        'members' : memberPlayerTag})
        
        #return the html page
        self.response.out.write(html)
    
app = webapp2.WSGIApplication([ ('/teams', TeamRequestHandler),], debug=True)  
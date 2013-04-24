import webapp2
import jinja2 
import os
import functions
import model 

from google.appengine.ext import ndb
##==============================================================================##
##    Joinateam.py Join a Team                                                  ##
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

class JoinATeamHandler(webapp2.RequestHandler):    #Web Page Index Handler Class
        
    def post(self):
        template = jinja_environment.get_template('templates/joinateam.html')
        teamKey = ndb.Key(urlsafe=self.request.get('selectedTeam')).get()
        playerTagKey = functions.Worker.PlayerTagStringToPlayerKey(self.request.get('currentUser'))
        
        #Check if this user is part of this current team
        teamMember = functions.Worker.GetPlayerTagTeamList(playerTagKey)
        if(teamMember.__contains__(teamKey)):
            html = template.render({'the_title': 'Join A Team.',
                                    'playerTagHeader': playerTagKey.tag,
                                    'errorMatch': 'Player Tag is already a member of this Team!',
                                    'teams' : model.Team.query()})
        else:
            teamKey.members.append(playerTagKey.key)
            teamKey.put()
            
            team = functions.Worker.GetPlayerTagTeamList(playerTagKey)
            friends = functions.Worker.GetFriendsList(playerTagKey)
            
            template = jinja_environment.get_template('templates/dash.html')
            html = template.render({'playerTagHeader': playerTagKey.tag,
                                    'teams' : team,
                                    'the_title': 'Dashboard',
                                    'friends' : friends})
        
        #return the html page
        self.response.out.write(html)
            
app = webapp2.WSGIApplication([ ('/joinateam', JoinATeamHandler),], debug=True)  
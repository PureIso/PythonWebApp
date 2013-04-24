import webapp2
import jinja2 
import os
import functions

from google.appengine.ext import ndb
##==============================================================================##
##    ManageATeam.py Manage a team                                              ##
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

class ManageATeamHandler(webapp2.RequestHandler):    #Web Page Index Handler Class
        
    def post(self):
        template = jinja_environment.get_template('templates/manageateam.html')
        
        currentUser = functions.Worker.PlayerTagStringToPlayerKey(self.request.get('currentUser'))
        currentTeam = functions.Worker.TeamStringToTeamKey(self.request.get('currentTeam'))
        removeMemberKey = self.request.get('selectedMember')
        removeMemberKey = ndb.Key(urlsafe=removeMemberKey).get()

        members = functions.Worker.GetTeamMembersList(currentTeam)
        memberPlayerTag = []
        for member in members:
            member = functions.Worker.PlayerTagStringToPlayerKey(member)
            memberPlayerTag.append(member)   
         
        if(currentTeam.administrator != currentUser.key):
            html = template.render({'the_title': 'Manage A Team.',
                                    'playerTagHeader': currentUser.tag,
                                    'errorMatch': 'Administrators privilege required in order to remove members.',
                                    'team' : currentTeam.teamName,
                                    'members' : memberPlayerTag})
        else:   
            if(currentTeam.administrator == removeMemberKey.key):
                html = template.render({'the_title': 'Manage A Team.',
                                        'playerTagHeader': currentUser.tag,
                                        'errorMatch': 'Administrators cannot be removed. Delete the Team instead!',
                                        'team' : currentTeam.teamName,
                                        'members' : memberPlayerTag})
            else: 
                currentTeam.members.remove(removeMemberKey.key)
                currentTeam.put()
            
                team = functions.Worker.GetPlayerTagTeamList(currentUser)
                friends = functions.Worker.GetFriendsList(currentUser)
                template = jinja_environment.get_template('templates/dash.html')
                html = template.render({'playerTagHeader': currentUser.tag,
                                        'teams' : team,
                                        'the_title': 'Dashboard',
                                        'friends' : friends})   
              
        #return the html page
        self.response.out.write(html)
            
app = webapp2.WSGIApplication([ ('/manageateam', ManageATeamHandler),], debug=True)  
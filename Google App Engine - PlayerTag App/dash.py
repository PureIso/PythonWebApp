import webapp2
import jinja2 
import os
import functions

##==============================================================================##
##    Dash.py This is the dashboard after login                                 ##
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

class DashRequestHandler(webapp2.RequestHandler):    #Web Page Index Handler Class
        
    def post(self):
        the_Page = self.request.get('page')
        
        playerTagKey = functions.Worker.PlayerTagStringToPlayerKey(self.request.get('currentUser'))
        friends = functions.Worker.GetFriendsList(playerTagKey)
        team = functions.Worker.GetPlayerTagTeamList(playerTagKey)
                       
        #If friend request option selected
        if(the_Page == 'friendRequest'):
            notFriendsWith = functions.Worker.NonFriendsList(playerTagKey)
            if (notFriendsWith.__len__() == 0):
                template = jinja_environment.get_template('templates/dash.html')
                html = template.render({'the_title': 'Dashboard',
                                        'errorMatch': 'You are friends with everyone or Your Request/s are Pending !',
                                        'playerTagHeader' : playerTagKey.tag,
                                        'teams' : team,
                                        'friends': friends})
            else:        
                template = jinja_environment.get_template('templates/friendRequest.html')
                html = template.render({'the_title': 'Friend Request',
                                        'PlayerTags': notFriendsWith,
                                        'playerTagHeader': playerTagKey.tag,})
        
        #If pending Request option selected    
        elif (the_Page == 'pendingRequest'):
            requestPendingList = functions.Worker.GetPendingRequestList(playerTagKey)
            if(requestPendingList.__len__() == 0):
                template = jinja_environment.get_template('templates/dash.html')
                html = template.render({'the_title': 'Dashboard',
                                        'errorMatch': 'No Request Pending',
                                        'playerTagHeader' : playerTagKey.tag,
                                        'teams' : team,
                                        'friends': friends})
            else:
                template = jinja_environment.get_template('templates/'+the_Page+'.html')
                html = template.render({'query': requestPendingList,
                                        'the_title': 'Pending Request',
                                        'playerTagHeader': playerTagKey.tag,})
        #If Team set up is selected
        else:
            template = jinja_environment.get_template('templates/teams.html')
            html = template.render({'playerTagHeader': playerTagKey.tag,
                                    'the_title': 'Teams', 
                                    'teams' : team})
        
        #return the html page
        self.response.out.write(html)
    
app = webapp2.WSGIApplication([ ('/dash', DashRequestHandler),], debug=True)                         #Call by the app.yaml


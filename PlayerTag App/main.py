import cherrypy
import jinja2
import os
import webbrowser
import sys
import model
import functions

from dash import Dash
from register import Register
from friendRequest import FriendRequest
from pendingRequest import PendingRequest
from teams import TeamRequest
from manageateam import ManageATeam
from joinateam import JoinATeam
from createnewteam import CreateNewTeam

##==============================================================================##
##    Main.py Displays the Main Home Screen                                     ##
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

class Root(object):
    def POST(self, playerTag, password):
        template = jinja_environment.get_template('templates/main.html')
        try:
            connection = functions.Worker()
        except:
            return template.render({'the_title': 'Main',
                                'errorMatch': ("Unexpected error:", sys.exc_info()[1])
                                }) 
        if(password == None or str(password) == "") :
            return template.render({'the_title': 'Main',
                                    'errorMatch': 'Empty Password'}) 
        elif(playerTag == None or str(playerTag) == "") :
            return template.render({'the_title': 'Main',
                                    'errorMatch': 'Empty playerTag'})
        else:
            playerTagObject = model.PlayerTag()                                  
            playerTagObject.SetPlayerTag(playerTag)
            playerTagObject.SetPassword(password)
            
            if (connection.FindPlayerTag(playerTagObject).count() > 0):
                #Start Session
                cherrypy.session['PlayerTag'] = playerTagObject.GetPlayerTag()
                root.friendRequest.PlayerTag = playerTagObject.GetPlayerTag()
                
                raise cherrypy.HTTPRedirect("/dash/", 302)
            else:
                return template.render({'the_title': 'Main',
                                        'errorMatch': 'Invalid playerTag or password'})
        
    
    def GET(self):
        cherrypy.lib.sessions.expire()
        template = jinja_environment.get_template('templates/main.html')   
        return template.render({'the_title': 'Main'})
    
    @cherrypy.expose
    def index(self, playerTag=None, password=None):
        if(cherrypy.request.method == 'GET'):
            return self.GET()
        else:
            return self.POST(playerTag, password)
        

#Forces the browser to startup, easier for development
def open_browser():
    webbrowser.open("http://127.0.0.1:8080/")   

#Directory Setup
root = Root()
root.dash = Dash()
root.register = Register()
root.friendRequest = FriendRequest()
root.pendingRequest = PendingRequest()
root.teams = TeamRequest()
root.manageateam = ManageATeam()
root.joinateam = JoinATeam()
root.createnewteam = CreateNewTeam()

#Initialize Main
if __name__ == '__main__':
    # Our location
    base_dir = os.path.abspath(os.path.dirname(__file__))
    # Our conf directory
    conf_path = os.path.join(base_dir, "conf")
    # to create the logs directory
    log_dir = os.path.join(base_dir, "logs")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    
    cherrypy.engine.subscribe('start', open_browser)   
    cherrypy.tree.mount(root,'/', os.path.join(conf_path, "app.cfg"))
    cherrypy.engine.start()
import webapp2
import jinja2 
import os
import functions

##==============================================================================##
##    Main.py Displays the Main Home Screen                                     ##
##==============================================================================##
##      Author:         C00117798 - Olawale Egbeyemi                            ##
##      Date:           11/12/2010                                              ##
##      Last Modified:  29/12/2012                                              ##
##      Description:                                                            ##
##      Python Version:  2.7                                                    ##
##      NB:                                                                     ##
##==============================================================================##
##==============================================================================##

#Global Variable
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class IndexPageHandler(webapp2.RequestHandler):    #Web Page Index Handler Class
    
    def get(self):                          	   #Default method that is called
        the_path = self.request.path               #Working out the path that was sent
        
        if the_path == '/': the_path = '/main'     #If the path is just /
            
        template = jinja_environment.get_template('templates' + the_path + '.html')     #Get the html url and set it to template
        html = template.render({'the_title': 'Home'})
        self.response.out.write(html)
    
    def post(self):
        template = jinja_environment.get_template('templates/main.html')
        
        #If valid sign in
        if(functions.Worker.SignInPlayer(self.request.get('playerTag'), self.request.get('password'))):
            playerTagKey = functions.Worker.PlayerTagStringToPlayerKey(self.request.get('playerTag'))
            friends = functions.Worker.GetFriendsList(playerTagKey)
            team = functions.Worker.GetPlayerTagTeamList(playerTagKey)
            
            template = jinja_environment.get_template('templates/dash.html')
            html = template.render({'the_title': 'Dashboard',
                                    'playerTagHeader' : playerTagKey.tag,
                                    'teams' : team,
                                    'friends': friends})
        else:
            html = template.render({'errorMatch': 'Invalid Player Tag/Password or Account/Player Tag waiting for confirmation'})
        
        #return the html page
        self.response.out.write(html)

app = webapp2.WSGIApplication([ ('/.*', IndexPageHandler),], debug=True)                         #Call by the app.yaml

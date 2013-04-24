import webapp2
import model
import jinja2 
import os
import mailer

from google.appengine.api import users
import functions
##==============================================================================##
##    Register.py Register a Player Tag                                         ##
##==============================================================================##
##      Author:         C00117798 - Olawale Egbeyemi                            ##
##      Date:           11/12/2010                                              ##
##      Last Modified:  13/01/2013                                              ##
##      Description:                                                            ##
##      Python Version:  2.7                                                    ##
##==============================================================================##
##==============================================================================##

#Global Variable
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class RegisterHandler(webapp2.RequestHandler):

    def get(self):
        template = jinja_environment.get_template('templates/register.html')
        self.response.out.write(template.render({ 'the_title': 'Register'}))
     
    def post(self):
        the_tag = self.request.get('playerTag')                                     #The Player Tag                  
        the_password = self.request.get('password')                                 #Login Password
        the_confirmPassword = self.request.get('confirmPassword')                   #Confirm Password
        
        if( the_password != the_confirmPassword):                                   #Compare passwords
            template = jinja_environment.get_template('templates/register.html')
            html = template.render({'errorMatch': 'Password Mismatch'})             
        else:
            playerTag = model.PlayerTag()                                           #Create a new Instance
            playerTag.tag = the_tag                                                 #Assign Values
            playerTag.password = the_password
            playerTag.google_id = users.get_current_user()                          #Get current logged in user from google user api
            playerTag.activationToken = functions.Worker.TokenGenerator()
            playerTag.confirm = False
            
            #Check for duplicates                                              
            query = model.PlayerTag.query(model.PlayerTag.tag == playerTag.tag)
            if(query.count() > 0 ):
                template = jinja_environment.get_template('templates/register.html')
                html = template.render({'errorPlayerTag': 'Duplicate Player Tags'})             #Look for a value called name
            else:
                template = jinja_environment.get_template('templates/main.html')                #Get the html url and set it to template
                html = template.render({'the_title': 'Home'})
                playerTag.put()                                                                                            #Write entity into datastore
                mailer.ConfirmationEmail(playerTag.google_id.nickname(), playerTag.tag, playerTag.activationToken)         #Email the Google id
                
        #return the html page        
        self.response.out.write(html)
           
app = webapp2.WSGIApplication([ ('/register', RegisterHandler),], debug=True)

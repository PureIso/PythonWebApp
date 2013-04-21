import cherrypy
import jinja2
import os
import sys
import model
import functions
##==============================================================================##
##    Register.py Allow users to register a playerTag                           ##
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

class Register(object):
    def POST(self,password, confirmPassword, playerTag):
        template = jinja_environment.get_template('templates/register.html')
        try:
            connection = functions.Worker()                                     # get an instance of the class
        except:
            return template.render({'the_title': 'Register',
                                    'errorOther': ("Unexpected error:", sys.exc_info()[1])
                                    }) 
            
        if( password != confirmPassword):                                   #Compare passwords
            return template.render({'the_title': 'Register',
                                    'errorPassword': 'Password Mismatch',
                                    'errorCPassword': 'Password Mismatch'})  
        elif(password == None or str(password) == "" ) :
            return template.render({'the_title': 'Register',
                                    'errorPassword': 'Empty Password'}) 
        elif(playerTag == None or str(playerTag) == "")  :
            return template.render({'the_title': 'Register',
                                    'errorPlayerTag': 'Empty playerTag'}) 
                   
        else:
            playerTagObject = model.PlayerTag()                                  
            playerTagObject.SetPlayerTag(playerTag)
            playerTagObject.SetPassword(password)
            
            if (connection.FindPlayerTag(playerTagObject).count() > 0): #Find the player tag
                return template.render({'the_title': 'Register',
                                        'errorOther': "Player Tag already exists!"})
            else:
                connection.InsertPlayerTag(playerTagObject)
                raise cherrypy.HTTPRedirect("/", 302)
        
    
    def GET(self):
        template = jinja_environment.get_template('templates/register.html')   
        return template.render({'the_title': 'Register'})
    
    @cherrypy.expose
    def index(self,password=None, confirmPassword=None, playerTag=None):
        if(cherrypy.request.method == 'GET'):
            return self.GET()
        else:
            return self.POST(password,confirmPassword, playerTag)
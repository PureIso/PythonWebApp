import webapp2
import model
from google.appengine.api import mail

##==============================================================================##
##    Admin_Mail.py Accept Email and store in datastore                         ##
##==============================================================================##
##      Author:         C00117798 - Olawale Egbeyemi                            ##
##      Date:           11/12/2010                                              ##
##      Last Modified:  13/01/2013                                              ##
##      Description:                                                            ##
##      Python Version:  2.7                                                    ##
##==============================================================================##
##==============================================================================##

class AdminMailHandler(webapp2.RequestHandler):
    def post(self):
        message = mail.InboundEmailMessage(self.request.body)                   #Accept in bound mails

        new_email = model.EmailArchive()                                        #Set a new EmailArchieve entity
        new_email.from_ = message.sender                                        
        new_email.subject = message.subject
        
        email_body = list(message.bodies(content_type='text'))[0]
        new_email.content = str(email_body[1])                                  #convert the message into readable string
        
        startIndex = 1+new_email.from_.index('<')
        endIndex = new_email.from_.index('@')
        newString = new_email.from_[startIndex:endIndex]
        
        query = model.PlayerTag.query()
        
        for item in query: 
            if(item.confirm == False and str(item.google_id) == newString and new_email.subject.__contains__(item.activationToken)):
                item.confirm = True
                item.put()
                new_email.put()

app = webapp2.WSGIApplication( [ ( '/.*', AdminMailHandler ) ], debug=True )


from google.appengine.api import mail

##==============================================================================##
##    Mailer.py Send Email to google Mail                                       ##
##==============================================================================##
##      Author:         C00117798 - Olawale Egbeyemi                            ##
##      Date:           11/12/2010                                              ##
##      Last Modified:  13/01/2013                                              ##
##      Description:                                                            ##
##      Python Version:  2.7                                                    ##
##==============================================================================##
##==============================================================================##

def ConfirmationEmail(destination, playerTag, token): 
    sender = 'Admin at c00117798-a2(Game System) <admin@c00117798-a2.appspotmail.com>' 
    subject = 'The c00117798-a2 Game System - Confirmation - %s' % (token) 
    #Replace %s with (playerTag)
    body = """Hi!
    
    Thank you for registering for The c00117798-a2 Game System Application.
    Your Player Tag is: %s.
    Your Activation Token is: %s
    
    Please reply to this email to confirm your Player Tag.
    Also make sure the subject contains the Activation Token.
    
    Thanks, 
    The c00117798-a2 Game System Application Team.
    """ % (playerTag, token)                               

    email_to = destination + '@gmail.com'
    mail.send_mail(sender, email_to, subject, body)

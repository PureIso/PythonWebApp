import webapp2
import jinja2 
import os
import model
import functions
from google.appengine.ext import ndb

##==============================================================================##
##    PendingRequest.py Accept of Decline Pending Friend Request                ##
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

class PendingRequestHandler(webapp2.RequestHandler):    #Web Page Index Handler Class
    def post(self):                  
        currentUserKey = functions.Worker.PlayerTagStringToPlayerKey(self.request.get('currentUser'))
        fromPlayerTagKey = self.request.get('requestPending')
        decission = self.request.get('button')
        
        #Get keys               
        fromPlayerTagKey = ndb.Key(urlsafe=fromPlayerTagKey).get()
        
        #Get friend request object
        query = model.FriendsRequest.query(model.FriendsRequest.fromTag == fromPlayerTagKey.key,
                                           model.FriendsRequest.toTag == currentUserKey.key,
                                           model.FriendsRequest.confirmation == 'Awaiting')
        
        #Get the object
        friendRequest = model.FriendsRequest()
        for item in query:
            friendRequest = item
        
        #Get the player Tag request is from
        query = model.PlayerTag.query(model.PlayerTag.key == fromPlayerTagKey.key)
        for item in query:
            fromPlayerTag = item
        
        friends = functions.Worker.GetFriendsList(currentUserKey)
        if(decission == 'Accept'):
            if(friends.__contains__(fromPlayerTagKey)):return
            
            friendRequest.confirmation = 'Accept'

            currentUserKey.friends.append(fromPlayerTagKey.key)
            fromPlayerTag.friends.append(currentUserKey.key)
            
            friendRequest.put()
            currentUserKey.put()
            fromPlayerTag.put()
        else:
            friendRequest.confirmation = 'Decline'
            friendRequest.put()
            
        friends = functions.Worker.GetFriendsList(currentUserKey)
        template = jinja_environment.get_template('templates/dash.html')
        html = template.render({'playerTagHeader': currentUserKey.tag,
                                'the_title': 'Dashboard',
                                'friends' : friends})
        
        #return the html page
        self.response.out.write(html)
        
        
app = webapp2.WSGIApplication([ ('/pendingRequest', PendingRequestHandler),], debug=True) #Call by the app.yaml


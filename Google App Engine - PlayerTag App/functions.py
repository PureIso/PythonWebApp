from google.appengine.ext import ndb
import model
import string
import random

class Worker():
    #Convert String PlayerTag to the object PlayerTag
    @staticmethod
    def PlayerTagStringToPlayerKey(playerNameString):
        query = model.PlayerTag.query(model.PlayerTag.tag == playerNameString)
        the_CurrentUser = ""
        for item in query:
            the_CurrentUser = item.key.urlsafe()                            #make key url safe
            the_CurrentUser = ndb.Key(urlsafe=the_CurrentUser).get()        #CurrentUser Key
        return the_CurrentUser
    
    #Convert String PlayerTag Key to the Object PlayerTag
    @staticmethod
    def PlayerKeyToPlayerTag(playerKey):
        query = model.PlayerTag.query(model.PlayerTag.key == playerKey)
        the_CurrentUser = model.PlayerTag() 
        for item in query:
            the_CurrentUser = item
        return the_CurrentUser
    
    #Convert String Team Key to Team Object
    @staticmethod
    def TeamStringToTeamKey(teamNameString):
        query = model.Team.query(model.Team.teamName == teamNameString)
        currentTeam = ""
        for item in query:
            currentTeam = item.key.urlsafe()
            currentTeam = ndb.Key(urlsafe=currentTeam).get()        
        return currentTeam
    
    #Get Friends of the specified PlayerTag
    @staticmethod
    def GetFriendsList(playerTagKey):
        friends = []
        query = model.PlayerTag.query(model.PlayerTag.tag == playerTagKey.tag, 
                                      model.PlayerTag.confirm == True)
        if(query.count() > 0):
            for tag in query:
                for friend in tag.friends:
                    #Convert key to player Tag
                    newQuery = model.PlayerTag.query(model.PlayerTag.key == friend)
                    for playerTag in newQuery:
                        friends.append(playerTag)      #Append key since friends is a key property
        return friends
    
    #Get the list of teams the playerTag is a member of
    @staticmethod
    def GetPlayerTagTeamList(playerTagKey):
        teams = []
        query = model.Team.query()
        
        if(query.count() > 0):
            for team in query:
                for member in team.members:
                    newQuery = model.PlayerTag.query(model.PlayerTag.key == member)
                    if(newQuery.count > 0):
                        for player in newQuery:
                            if(player.key == playerTagKey.key):
                                teams.append(team)
        return teams
    
    #Get the members of the specified team
    @staticmethod
    def GetTeamMembersList(team):
        teamMembers = []
        query = model.Team.query(model.Team.key == team.key)
        
        if(query.count() > 0):
            for team in query:
                for member in team.members:
                    newQuery = model.PlayerTag.query(model.PlayerTag.key == member)
                    if(newQuery.count > 0):
                        for player in newQuery:
                            teamMembers.append(player.tag)
        return teamMembers  
    
    #Get a list of Player Tags not friends with the specified PlayerTagKey
    @staticmethod
    def NonFriendsList(playerTagKey):
        friendsKeys = []
        notFriendsWith = []
        
        #Get current friends
        query = model.PlayerTag.query(model.PlayerTag.tag == playerTagKey.tag, 
                                      model.PlayerTag.confirm == True)
        
        if(query.count() > 0):
            for tag in query:
                for friend in tag.friends:
                    friendsKeys.append(friend)      #Append key since friends is a key property
        
        #Get all who you are not friends with
        query = model.PlayerTag.query(model.PlayerTag.confirm == True, model.PlayerTag.tag != playerTagKey.tag)
        if(query.count() > 0):
            for tag in query:
                if( not friendsKeys.__contains__(tag.key)):
                    notFriendsWith.append(tag)
                 
        #Get all who are pending
        #NB: The person you send a request to can still send you a request but you can't  - while pending
        query = model.FriendsRequest.query( model.FriendsRequest.confirmation == "Awaiting",
                                            model.FriendsRequest.fromTag == playerTagKey.key)
        
        if(query.count() > 0):
            for tag in query:
                #Convert key to player Tag
                newQuery = model.PlayerTag.query(model.PlayerTag.key == tag.toTag)
                for playerTag in newQuery:
                    if(notFriendsWith.__contains__(playerTag)):
                        notFriendsWith.remove(playerTag)
                        
        return notFriendsWith
    
    #Get the list of PlayerTag pending Friends request for the specified Player Tag
    @staticmethod
    def GetPendingRequestList(playerTagKey):
        items = []
        #Query for all the request for the current user
        query = model.FriendsRequest.query(model.FriendsRequest.toTag == playerTagKey.key,
                                           model.FriendsRequest.confirmation == "Awaiting",
                                           model.FriendsRequest.fromTag != playerTagKey.key)
        if(query > 0):
            #each request
            for item in query:  #query = FriendRequest
                #Query for any player with the key
                playerQuery = model.PlayerTag.query(model.PlayerTag.key == item.fromTag)
                if(playerQuery > 0):                    #if we have a value
                    for innerItem in playerQuery:       #We now have the PlayerTag'
                        items.append(innerItem)         #Append the PlayerTag to the items List
        return items
    
    #Verify the login using the PlayerTag and password
    @staticmethod
    def SignInPlayer(playerTagString, password):
        query = model.PlayerTag.query(model.PlayerTag.tag == playerTagString,
                                      model.PlayerTag.password == password)
        
        if (query.count() > 0):
            newQuery = model.PlayerTag.query(model.PlayerTag.tag == playerTagString,
                                             model.PlayerTag.password == password,
                                             model.PlayerTag.confirm == True)
            if(newQuery.count() > 0):
                return True
            else:
                return False
        else:
            return False
        
    #Random Token Generator
    @staticmethod
    def TokenGenerator(size=12, chars=string.ascii_uppercase + string.digits):
        token =''.join(random.choice(chars) for _ in range(size))
        query = model.PlayerTag.query()

        for item in query:
            while (str(item.activationToken) == token):
                token =''.join(random.choice(chars) for _ in range(size))
        return token
    
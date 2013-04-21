from pymongo import Connection

class Worker():
    def __init__(self):
        connection = Connection()
        db = connection.gamesite
        self.playerTags = db.PlayerTags
        self.teams = db.Teams
        self.friendsRequests = db.FriendsRequests
    
    #============================================================#
    ###     Insert
    #============================================================#
    def InsertPlayerTag(self,playerTag):
        self.playerTags.save(playerTag.__dict__)
    
    def UpdatePlayerTag(self,playerTag):
        q = self.playerTags.find_one({'PlayerTag' : playerTag['PlayerTag']})                          
        self.playerTags.update(q, 
                                    {'$set': {'Friends': playerTag['Friends'],
                                              'Teams': playerTag['Teams'],}},
                                    True)
           
    def InsertTeam(self,team):
        self.teams.save(team.__dict__)
    
    def UpdateTeam(self,team):
        q = self.teams.find_one({'TeamName' : team['TeamName']})                          
        self.teams.update(q, 
                          {'$set': {'Members': team['Members']}},
                          True)
        
    def InsertFriendRequest(self,friendRequest):
        self.friendsRequests.save({'FromTag' : friendRequest.GetFromTag(),
                                   'ToTag' : friendRequest.GetToTag(),
                                   'Confirmation': friendRequest.GetConfirmation()})
    
    def UpdateFriendRequest(self,friendRequest): 
        q = self.friendsRequests.find_one({'FromTag' : friendRequest['FromTag'],
                                       'ToTag' : friendRequest['ToTag']})                             
        self.friendsRequests.update(q, 
                                    {'$set': {'Confirmation': friendRequest['Confirmation']}},
                                    True)
                               
    #============================================================#
    ###     Find
    #============================================================#
    def FindPlayerTag(self,playerTag):
        return self.playerTags.find({'PlayerTag' : playerTag.PlayerTag,
                                     'Password' : playerTag.Password})
        
    def FindTeam(self,teamName):
        return self.teams.find_one({'TeamName' : teamName.GetTeamName(),})
    
    def FindPlayerTagNoPass(self,playerTag):
        return self.playerTags.find_one({'PlayerTag' : playerTag.GetPlayerTag()})
        
    def FindFriendRequestDuplicate(self,friendRequest):
        requests = []
        if(self.friendsRequests.find().count() == 0):
            return requests
        else:
            for request in self.friendsRequests.find({'FromTag' : friendRequest.GetFromTag(),
                                                      'ToTag' : friendRequest.GetToTag()}):
                requests.append(request)
            return requests
    
    def FindFriendRequest(self,friendRequest):
        requests = []
        for request in self.friendsRequests.find({'FromTag' : friendRequest.FromTag.GetPlayerTag(),
                                                  'ToTag' : friendRequest.ToTag.GetPlayerTag(),
                                                  'Confirmation': "Awaiting"}):
            requests.append(request)
        for request in self.friendsRequests.find({'FromTag' : friendRequest.FromTag.GetPlayerTag(),
                                                  'ToTag' : friendRequest.ToTag.GetPlayerTag(),
                                                  'Confirmation': "Decline"}):
            requests.append(request)
        return request



    #============================================================#
    #     Others
    #============================================================#
    def GetFriends(self,playerTag):
        player = self.playerTags.find_one({'PlayerTag' : playerTag.GetPlayerTag()})
        friends = []
        for item in player['Friends']:
            friends.append(item)
        return friends
    
    def GetTeams(self,playerTag):
        player = self.playerTags.find_one({'PlayerTag' : playerTag.GetPlayerTag()})
        teams = []
        for item in player['Teams']:
            teams.append(item)
        return teams
    
    def GetAllTeams(self):
        teams = []
        for item in self.teams.find():
            teams.append(item['TeamName'])
        return teams
    
    def GetAllRequestPending(self,playerTag):
        requests = []
        for request in self.friendsRequests.find({'$or': [{'ToTag' : playerTag.PlayerTag},
                                                          {'FromTag' : playerTag.PlayerTag}],
                                                  'Confirmation': "Awaiting"}):
            requests.append(request)
        return requests
    
    def GetRequestPendingFor(self,playerTag):
        requests = []
        for request in self.friendsRequests.find({'ToTag' : playerTag.PlayerTag,
                                                  'Confirmation': "Awaiting"}):
            requests.append(request)
        return requests
    
    
    
    def GetRequestPendingForFrom(self,fromTag,toTag):
        requests = []
        for request in self.friendsRequests.find({'ToTag' : toTag['PlayerTag'],
                                                  'FromTag' : fromTag['PlayerTag'],
                                                  'Confirmation': "Awaiting"}):
            requests.append(request)
        return requests
    
    ##Get a list of players not on your friends list
    def NonFriendsList(self,playerTag):
        notFriendsWith = []
        friends =[]
        
        #Get current friends
        q = self.FindPlayerTagNoPass(playerTag)
        for item in q['Friends']:
            friends.append(item)
        
        #Get all who you are not friends with
        allPlayers = []
        for player in self.playerTags.find():
            allPlayers.append(player)
        
        if(allPlayers.__len__() > 0):
            for item in allPlayers:
                if(friends.__contains__(item['PlayerTag'])):continue
                elif(playerTag.PlayerTag == item['PlayerTag']):continue #dictionary syntax
                else: notFriendsWith.append(item['PlayerTag'])  
                     
        #Get and removing pending request
        requests = self.GetAllRequestPending(playerTag)
        if(requests.__len__() > 0):
            for request in requests:
                if(notFriendsWith.__contains__(request['FromTag'])):
                    notFriendsWith.remove(request['FromTag'])
                if(notFriendsWith.__contains__(request['ToTag'])):
                    notFriendsWith.remove(request['ToTag'])   
        return notFriendsWith
    
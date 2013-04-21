
class PlayerTag(object):
    def __init__(self,playerTag=None,password=None):
        self.PlayerTag = playerTag
        self.Password = password
        self.Friends = []
        self.Teams = []
    def GetPlayerTag(self):
        return str(self.PlayerTag)
    def SetPlayerTag(self,playerTag):
        self.PlayerTag = playerTag 
    def GetPassword(self):
        return self.Password
    def SetPassword(self,password):
        self.Password = password
    def GetFriends(self):
        return self.Friends
    def AddAFriend(self,playerTag):
        self.Friends.append(playerTag)
    def GetTeams(self):
        return self.Teams
    def AddATeam(self,team):
        self.Teams.append(team)     

class Team(object):
    def __init__(self,administrator=None,teamName=None):
        self.Administrator = administrator
        self.TeamName = teamName
        self.Members = []
    def GetAdministrator(self):
        return str(self.Administrator)
    def SetAdministrator(self,administrator):
        self.Administrator = administrator 
    def GetTeamName(self):
        return self.TeamName
    def SetTeamName(self,teamName):
        self.TeamName = teamName
    def GetMembers(self):
        return self.Members
    def SetMembers(self,members):
        self.Members.append(members)
        
class FriendsRequest(object):
    def __init__(self,fromTag=None,toTag=None,confirmation=None):
        self.FromTag = fromTag
        self.ToTag = toTag
        self.Confirmation = confirmation
        
    def GetFromTag(self):
        return self.FromTag
    def SetFromTag(self,fromTag):
        self.FromTag = fromTag 
        
    def GetToTag(self):
        return self.ToTag
    def SetToTag(self,toTag):
        self.ToTag = toTag
        
    def GetConfirmation(self):
        return self.Confirmation
    def SetConfirmation(self,confirmation):
        self.Confirmation = confirmation
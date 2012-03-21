'''
Created on Mar 21, 2012

@author: DreamBit
'''
import urllib2, base64, json, threading, time
class githubConnector:
    def __init__(self, login="", password="", OAuthToken=None):
        self.login = login
        self.password = password
        self.OAuthToken = OAuthToken
        
    
    def getRepositories(self, organizationName=""):
        if self.OAuthToken is None:
            #Link for getting all repositories in the company
            url = "https://api.github.com/orgs/%s/repos" % organizationName
            #Converting login and password to base64
            base64string = base64.encodestring('%s:%s' % (self.login, self.password))[:-1]
            #Creating request
            req = urllib2.Request(url)
            #Adding the login and password in the request header
            req.add_header("Authorization", "Basic %s" % base64string)
            try:
                #Trying to send a request
                handle = urllib2.urlopen(req)
                #Response
                response = handle.read()
                
                jsonview = json.loads(response)
                #Return list of repositories names
                return [x['name'] for x in jsonview]
            except IOError:
                print "Organization not found"
            
    def getTeams(self, repositoryName="", organizationName=""):
        if self.OAuthToken is None:
            #Link for getting all teams in the repository
            url = "https://api.github.com/repos/%s/%s/teams" % (organizationName, repositoryName)
            #Converting login and password to base64
            base64string = base64.encodestring('%s:%s' % (self.login, self.password))[:-1]
            #Creating request
            req = urllib2.Request(url)
            #Adding the login and password in the request header
            req.add_header("Authorization", "Basic %s" % base64string)
            try:
                #Trying to send a request
                handle = urllib2.urlopen(req)
                #Response
                response = handle.read()
                #Return json represent
                return [{'id': t['id'], 'name': t['name']} for t in json.loads(response)]
            except IOError:
                print "Organization or repository not found"
    
    def getUsers(self, teamID=""):
        if self.OAuthToken is None:
            #Link for getting all teams in the repository
            url = "https://api.github.com/teams/%s/members" % teamID
            #Converting login and password to base64
            base64string = base64.encodestring('%s:%s' % (self.login, self.password))[:-1]
            #Creating request
            req = urllib2.Request(url)
            #Adding the login and password in the request header
            req.add_header("Authorization", "Basic %s" % base64string)
            try:
                #Trying to send a request
                handle = urllib2.urlopen(req)
                #Response
                response = handle.read()
                
                jsonview = json.loads(response)
                #Return json represent
                return [x['login'] for x in jsonview]
            except IOError:
                print "Team not found"
    
class TeamGetterThread(threading.Thread):
        def __init__(self, gConnector, repository, organization, teams):
            threading.Thread.__init__(self)
            self.gConnector = gConnector
            self.repository = repository
            self.organization = organization
            self.teams = teams  
            #self.lock = threading.Lock()
            
        
        def run(self):
            t = self.gConnector.getTeams(repositoryName=self.repository, organizationName=self.organization)
            #self.lock.acquire(1)
            self.teams.append(t)
            #self.lock.release()
            print "Job done at", time.time()


class UserGetterThread(threading.Thread):
        def __init__(self, gConnector, teamID, users):
            threading.Thread.__init__(self)
            self.gConnector = gConnector
            self.teamID = teamID
            self.users = users  
            #self.lock = threading.Lock()
            
        
        def run(self):
            t = self.gConnector.getUsers(teamID = self.teamID)
            #self.lock.acquire(1)
            self.users.append(t)
            #self.lock.release()
            print "Job done at", time.time()
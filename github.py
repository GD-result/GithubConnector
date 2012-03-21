'''
Created on Mar 21, 2012

@author: Rezvan aka DreamBit aka John_Pa9JIbHuK

@organization: GridDynamics
'''
import urllib2, base64, json, threading, time
class githubConnector:
    def __init__(self, login, password, OAuthToken=None):
        '''
        Creates a connection to github.com
        
        @type login: String
        @type password: String
        @type OAuthToken: String   
        @param login: Your login on github.com
        @param password: Your password on github.com
        @param OAuthToken: Your OAuth token on github.com
        '''
        self.login = login
        self.password = password
        self.OAuthToken = OAuthToken
        
    
    def getRepositories(self, organizationName):
        '''
        Returns a list with the names of repositories in the company
        
        @type organizationName: String
        @param organizationName: Name of your organizationName
        @rtype: list
        @return: List of all repositories in organization
        '''
        #Authorization without OAuth token
        if self.OAuthToken is None:
            #Link for getting all repositories in the company
            url = "https://api.github.com/orgs/%s/repos" % organizationName
            #Converting login and password to base64
            base64string = base64.encodestring('%s:%s' % (self.login, self.password))[:-1]
            #Creating request
            requst = urllib2.Request(url)
            #Adding the login and password into the request header
            requst.add_header("Authorization", "Basic %s" % base64string)
            try:
                #Trying to send a request
                handle = urllib2.urlopen(requst)
                #Getting response
                response = handle.read()
                
                jsonview = json.loads(response)
                
                #Return list of repositories names
                return [x['name'] for x in jsonview]
            except IOError:
                print "Organization not found"
            
    def getTeams(self, repositoryName="", organizationName):
        '''
        
        '''
        #Authorization without OAuth token
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
    
    def getUsers(self, teamID):
        '''
        '''
        #Authorization without OAuth token
        if self.OAuthToken is None:
            #Link for getting all users in the repository
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
        def __init__(self, gConnector, repository, organization, teams, semaphore):
            threading.Thread.__init__(self)
            self.gConnector = gConnector
            self.repository = repository
            self.organization = organization
            self.semaphore = semaphore
            self.teams = teams  
            #self.lock = threading.Lock()
            
        
        def run(self):
            t = self.gConnector.getTeams(repositoryName=self.repository, organizationName=self.organization)
            #self.lock.acquire(1)
            self.teams.append(t)
            #self.lock.release()
            print "Job done at", time.time(), "Threads count ", len(threading.enumerate())
            self.semaphore.release()


class UserGetterThread(threading.Thread):
        def __init__(self, gConnector, teamID, users, semaphore):
            threading.Thread.__init__(self)
            self.gConnector = gConnector
            self.teamID = teamID
            self.users = users  
            self.semaphore = semaphore
            #self.lock = threading.Lock()
            
        
        def run(self):
            t = self.gConnector.getUsers(teamID = self.teamID)
            #self.lock.acquire(1)
            self.users.append(t)
            #self.lock.release()
            print "Job done at", time.time(), "Threads count ", len(threading.enumerate())
            self.semaphore.release()
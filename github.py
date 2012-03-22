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
            
    def getTeams(self, repositoryName, organizationName):
        '''
        Returns a list with the names of teams in the repository
        
        @type repositoryName: String
        @type organizationName: Strign
        @rtype: list
        @param repositoryName: Your repository name
        @param organizationName: Your organization name
        @return: List of all teams in repository
        Example return [{'id': 'name'}, {'id': 'name'}, ...]
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
                #Return new list with teams id and names
                return [{'id': t['id'], 'name': t['name']} for t in json.loads(response)]
            except IOError:
                print "Organization or repository not found"
    
    def getUsers(self, teamID):
        '''
        Returns a list with the names of users in the team
        
        @type teamID: String
        @rtype: list[][]
        @param teamID: Team's id
        @return: List of all users names in team
        Example return [['user1', 'user2', 'user3'], ['user6', 'user007'], ...]
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
                #Return new list with users logins
                return [x['login'] for x in jsonview]
            except IOError:
                print "Team not found"
    
class TeamGetterThread(threading.Thread):
    '''
    The class for getting a list of repositories in the company in a separate thread
    '''
    def __init__(self, gConnector, repository, organization, teams, semaphore, lock):
        '''
        @type gConnector: githubConnector
        @type repository: String
        @type organization: String
        @type teams: list
        @type semaphore: threading.Semaphore
        @type lock: threading.Lock
        
        @param gConnector: An instance of class githubConnector, which represents a connection to github.com
        @param repository: The name of the repository
        @param organization: The name of the organization
        @param teams: List, where will be added received teams
        @param semaphore: Semaphore, which will be released after work
        @param lock: Lock, for synchronous adding teams to list
        '''
        threading.Thread.__init__(self)
        
        self.gConnector = gConnector
        self.repository = repository
        self.organization = organization
        self.teams = teams
        
        self.semaphore = semaphore
        self.lock = lock
            
        
    def run(self):
        try:
            #Getting teams
            t = self.gConnector.getTeams(repositoryName=self.repository, organizationName=self.organization)
            
            #entrance to the protected area
            self.lock.acquire()
            #adding teams to list
            self.teams[self.repository] = t
            #exit from the protected area
            self.lock.release()
            print "Job done at", time.time(), "Threads count is ", len(threading.enumerate())
        except Exception:
            print "Fatal Error" 
        finally:
            self.semaphore.release()


class UserGetterThread(threading.Thread):
    '''
    The class for getting a list of users in the repository in a separate thread
    '''
    def __init__(self, gConnector, teamID, users, semaphore, lock):
        '''
        @type gConnector: githubConnector
        @type teamID: String
        @type users: list
        @type semaphore: threading.Semaphore
        @type lock: threading.Lock
        
        @param gConnector: An instance of class githubConnector, which represents a connection to github.com
        @param teamID: Identifier of the team
        @param users: List, where will be added received users
        @param semaphore: Semaphore, which will be released after work
        @param lock: Lock, for synchronous adding users to list
        '''
        threading.Thread.__init__(self)
        self.gConnector = gConnector
        self.teamID = teamID
        self.users = users  
        
        self.semaphore = semaphore
        self.lock = lock
            
        
    def run(self):
        try:
            #Getting uses from team
            t = self.gConnector.getUsers(teamID=self.teamID)
            #entrance to the protected area
            self.lock.acquire()
            #adding users to list
            self.users['users'] = t
            #exit from the protected area
            self.lock.release()
            #print "Job done at", time.time(), "Threads count ", len(threading.enumerate(), "\n")
            print "Job done at {0} Threads count - {1}".format(time.time(), threading.activeCount())
        except Exception:
            print "Fatal Error"
        finally:
            self.semaphore.release()

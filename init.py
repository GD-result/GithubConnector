'''
Created on 21.03.2012

@author: Rezvan
'''
from github import githubConnector
from github import TeamGetterThread
from github import UserGetterThread
from time import time
from time import sleep
import threading
#Creating the main github connector
git = githubConnector(login="login", password="password")
#Getting all repositories in organization
repositories = git.getRepositories(organizationName="organizationName")

teams = list()
thread = None
tim = time()
#Search of all repositories
for currentRepository in repositories:
    #teams.append(git.getTeams(repositoryName=repositories[i], organizationName="gd-result"))#
    
    #Creating a thread that will service a particular repository
    thread = TeamGetterThread(gConnector=git, 
                         repository=currentRepository, 
                         organization="gd-result", 
                         teams=teams)
    #Starting this thread
    thread.start()

#Waiting for the completion of all threads
while (len(threading.enumerate()) > 1):
    sleep(0.1)
    
print "Teams at ", time() - tim
users = list()
for i in xrange(0, len(teams)):
    for j in xrange(0, len(teams[i])):
        #users.append(git.getUsers(teams[i][j]['id']))
        thread = UserGetterThread(gConnector=git, 
                         teamID = teams[i][j]['id'],
                         users=users)
        thread.start()
        
while (len(threading.enumerate()) > 1):
    sleep(0.1)
print "Users at ", time() - tim
#print repositories
#print teams        
#print users
#
print "Rep count - %d" % len(repositories)
print "Teams count - %d" % len(teams)
print "Users count - %d" % len(users)
print time() - tim
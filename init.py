'''
Created on 21.03.2012

@author: Rezvan aka DreamBit aka John_Pa9JIbHuK

@organization: GridDynamics
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
users = list()

thread = None
semaphore = threading.Semaphore(10)
tim = time()
#Search of all repositories
for currentRepository in repositories:
    #teams.append(git.getTeams(repositoryName=repositories[i], organizationName="gd-result"))#
    
    #Creating a thread that will service a particular repository
    thread = TeamGetterThread(gConnector=git,
                         repository=currentRepository,
                         organization="organizationName",
                         teams=teams,
                         semaphore=semaphore)
    semaphore.acquire()
    #Starting this thread
    thread.start()

#Waiting for the completion of all threads
while (len(threading.enumerate()) > 1):
    sleep(0.1)
    
print "Teams at ", time() - tim
for i in xrange(0, len(teams)):
    for j in xrange(0, len(teams[i])):
        #users.append(git.getUsers(teams[i][j]['id']))
        thread = UserGetterThread(gConnector=git,
                         teamID=teams[i][j]['id'],
                         users=users,
                         semaphore=semaphore)
        semaphore.acquire()
        thread.start()
        
while (len(threading.enumerate()) > 1):
    sleep(0.1)
print "Users at ", time() - tim
#print repositories
#print teams        
#print users
#
print "Repositories count - %d" % len(repositories)
print "Teams count - %d" % len(teams)
print "Users count - %d" % len(users)
print "Final time ", time() - tim

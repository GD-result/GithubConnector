'''
Created on 21.03.2012

@author: Rezvan aka DreamBit aka John_Pa9JIbHuK

@organization: GridDynamics
'''
from github import githubConnector
from github import TeamGetterThread
from github import UserGetterThread
import wiki
from time import time
from time import sleep
import threading
#Creating the main github connector
git = githubConnector(login="login", password="pass")
#Getting all repositories in organization
repositories = git.getRepositories(organizationName="organizationName")
teams = {}

thread = None
semaphore = threading.Semaphore(10)
lock = threading.Lock()
tim = time()
#Search of all repositories
for currentRepository in repositories:   
    #Creating a thread that will service a particular repository
    thread = TeamGetterThread(gConnector=git,
                         repository=currentRepository,
                         organization="organizationName",
                         teams=teams,
                         semaphore=semaphore,
                         lock=lock)
    semaphore.acquire()
    #Starting this thread
    thread.start()

#Waiting for the completion of all threads
while (threading.activeCount() > 1):
    sleep(1)


for allteams in teams.values():
    for team in allteams:
        thread = UserGetterThread(gConnector=git,
                                  teamID=team['id'],
                                  users=team,
                                  semaphore=semaphore,
                                  lock=lock)
        semaphore.acquire()
        thread.start()
        
while (threading.activeCount() > 1):
    sleep(1)

repositories = teams 
print "Repositories count - %d" % len(repositories)
print "Final time ", time() - tim

wikiConnection = wiki.WikiConnector(wikiXMLRPCUrl="", 
                                    wikiLogin="", 
                                    wikiPassword="", 
                                    mainSpace="")

designContent = wikiConnection.createDesignContent(repositories)

wikiConnection.sendDesignContent(topPage="", pageName="", designContent=designContent)

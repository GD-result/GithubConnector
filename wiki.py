'''
Created on Mar 22, 2012

@author: Rezvan aka DreamBit aka John_Pa9JIbHuK

@organization: GridDynamics
'''
import xmlrpclib
class WikiConnector:
    '''
    Class for creating connection to wiki and working with XMLRPC
    '''
    def __init__(self, wikiXMLRPCUrl, wikiLogin, wikiPassword, mainSpace):
        '''
        Constructor
        '''
        self.XMLRPCUrl = wikiXMLRPCUrl
        self.Login = wikiLogin
        self.Password = wikiPassword
        self.mainSpace = mainSpace
        try:
            self.server = xmlrpclib.ServerProxy(self.XMLRPCUrl)
            self.token = self.server.confluence1.login(self.Login, self.Password)
        except xmlrpclib.Error:
            print "Fatal error"
        
    @staticmethod
    def createDesignContent(content):
        designContent = '''
                <table class = 'confluenceTable'>
                    <tr>
                        <th class='confluenceTh'>Repository</th>
                        <th class='confluenceTh'>Team</th>
                        <th class='confluenceTh'>User</th>
                    </tr>
            '''
        for repos in content.keys():
            designContent += "<tr> <td rowspan='%d' class='confluenceTd' style='font-weight: %s'>%s</td>"% (len(content[repos]), "bold", repos)
            for team in content[repos]:
                designContent += "<td class='confluenceTd'>%s</td>" % team['name']
                designContent += "<td class='confluenceTd'>%s</td>" % ",".join(team['users'])
                designContent += "</tr>"
        designContent += "</table>"   
        return designContent               
    
    
    def sendDesignContent(self, pageName, designContent):
        pass
    

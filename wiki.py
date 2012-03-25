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
        self.token = None
        self.server = None
        try:
            self.server = xmlrpclib.ServerProxy(self.XMLRPCUrl)
            self.token = self.server.confluence1.login(self.Login, self.Password)
        except xmlrpclib.Error:
            print "Fatal error"
        
    @staticmethod
    def createDesignContent(content):
        designContent = '''
                {html}
                <table class='confluenceTable'>
                    <tr>
                        <th class='confluenceTh'>Repository</th>
                        <th class='confluenceTh'>Teams</th>
                        <th class='confluenceTh'>Users</th>
                    </tr>
            '''
        for repos in content.keys():
            font = "bold" if repos[1] else "normal"
            designContent += "<tr> <td rowspan='%d' style='font-weight: %s' class='confluenceTd'>%s</td>"% (len(content[repos]), font, repos[0])
            for team in content[repos]:
                designContent += "<td class='confluenceTd'>%s</td>" % team['name']
                designContent += "<td class='confluenceTd'>%s</td>" % ",".join(team['users'])
                designContent += "</tr>"
        designContent += "</table>{html}"   
        return designContent               
    
    
    def sendDesignContent(self, topPage, pageName, designContent):
        try:
            page = self.server.confluence1.getPage(self.token, self.mainSpace, pageName)
        except:
            parentPage = self.server.confluence1.getPage(self.token, self.mainSpace, topPage)
            newPage = {
                      'parentId': parentPage['id'],
                      'space': self.mainSpace,
                      'title': pageName,
                      'content': designContent
                      }
            self.server.confluence1.storePage(self.token, newPage)
        else:
            page['content'] = designContent
            self.server.confluence1.updatePage(self.token, page, {'versionComment':'','minorEdit':1})

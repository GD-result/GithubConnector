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
    
    STYLE = {'admin': 'font-weight: bold; Color: #D53E07;',
             'push': 'font-weight: bold; Color: #006000;',
             'pull': 'font-weight: normal;'}
    
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
                *Repository* - private repository
                Repository - public repository 
                {color:#D53E07}*Team*{color} - team with pull, push & administrative access
                {color:#006000}*Team*{color} - team with push & pull access
                Team - team with pull only access
                h1. Github repositories
                {html}
                <div class='table-wrap'>
                <table width=50% class='confluenceTable'>
                    <tr>
                        <th class='confluenceTh'>Repository</th>
                        <th class='confluenceTh'>Teams</th>
                        <th class='confluenceTh'>Users</th>
                    </tr>
            '''
        rowColor = "#FBFFE8"
        for repos in content.keys():
            font = "bold" if repos[1] else "normal"
            designContent += "<tr> <td rowspan='%d' style='font-weight: %s; background-color: %s' class='confluenceTd'>%s</td>"% (len(content[repos]), font, rowColor, repos[0])
            if len(content[repos]) == 0:
                designContent += "<td class='confluenceTd' style='background-color: %s'> </td>" % rowColor
                designContent += "<td class='confluenceTd' style='background-color: %s'> </td>" % rowColor
            for team in content[repos]:
                designContent += "<td class='confluenceTd' style='%s background-color: %s'>%s</td>" % (WikiConnector.STYLE[team['permission']], rowColor, team['name'])
                designContent += "<td class='confluenceTd' style='background-color: %s'>%s</td>" % (rowColor, ", ".join(team['users']))
                designContent += "</tr>"
            rowColor = 'white' if rowColor == '#FBFFE8' else '#FBFFE8'
        designContent += "</table></div>{html}"   
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

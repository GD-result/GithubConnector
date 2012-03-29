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
                      
                        
    def sendContent(self, topPage, pageName, content, designer):
        '''
        Send content to wiki
        @type topPage: String
        @type pageName: String
        @type content: Some data(list, dict, ...)
        @type designer: Function
        @param topPage: Parent page of the page where you add content
        @param pageName: Page where you add content
        @param content: Crude version of the content that you want to send
        @param designer: A function that takes raw content and convert it into a formatted
        '''
        designerContent = designer(content)
        try:
            page = self.server.confluence1.getPage(self.token, self.mainSpace, pageName)
        except:
            parentPage = self.server.confluence1.getPage(self.token, self.mainSpace, topPage)
            newPage = {
                      'parentId': parentPage['id'],
                      'space': self.mainSpace,
                      'title': pageName,
                      'content': designerContent
                      }
            self.server.confluence1.storePage(self.token, newPage)
        else:
            page['content'] = designerContent
            self.server.confluence1.updatePage(self.token, page, {'versionComment':'','minorEdit':1})

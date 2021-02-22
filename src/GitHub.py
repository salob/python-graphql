'''
Created on 18 Feb 2021

@author: sianob
'''

import requests

class GitHub(object):
    '''
    Github object 
    '''


    def __init__(self,ghKey,apiUrl="https://api.github.com/graphql"):
        '''
        Constructor
        '''
        self.key = ghKey
        self.apiurl = apiUrl
        self.header={"Authorization": "Bearer "+self.key}
    
    def runQuery(self,query):
        request = requests.post(self.apiurl,headers=self.header,json={'query': query})
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
    
    def getIssueByNumber(self,owner,repo,issueNumber):
        query = """
            query{
              repository(owner: "%s" , name: "%s") {
                issue30: issue(number: %i) {
                  ...IssueFragment
                }
              }
            }
            
            fragment IssueFragment on Issue {
              title
              createdAt
              body
            }
        
        """ % (owner,repo,issueNumber)
        
        results = self.runQuery(query)
        
        return results

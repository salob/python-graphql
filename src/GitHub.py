
'''
Created on 18 Feb 2021

@author: salob
'''

import requests
from datetime import datetime

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
        s = requests.Session()
        request = s.post(self.apiurl,headers=self.header,json={'query': query})
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
    def getLabelByName(self,owner,repo,label):
        query = """
            query {
              repository(owner:"%s", name:"%s") {
                label(name:"%s") {
                  id
                }
              }
            }
        """ % (owner,repo,label)
        results = self.runQuery(query)

        return results
    #There should only be one actual release wiki issue per release ID
    def getIssueByExactTitle(self,owner,repo,label,issueTitle):
        issues = self.getIssuesByTitleKeywordAndLabel(owner,repo,label,issueTitle)
        for issue in issues['data']['search']['nodes']:
            if issue['title'] == issueTitle:
                return issue

    def getCommentByAuthorAndTitle(self,issue,commentAuthor,commentTitle):
        comments = issue['comments']['edges']
        for comment in comments:
            if comment['node']['body'].startswith(commentTitle) and comment['node']['author']['login'] == commentAuthor:
                return comment

    #returns list of issues containing keyword
    def getIssuesByTitleKeywordAndLabel(self,owner,repo,label,keyword):
        query = """
        {
          search(query: "repo:%s/%s label:\\"%s\\" in:title %s", type: ISSUE, first: 100) {
            nodes {
              ... on Issue {
                id
                number
                title
                body
                comments(first:100){
                    edges{
                        node{
                          id
                          author{
                            login
                          }
                          body
                        }
                    }
                }
              }
            }
          }
        }
        """ % (owner,repo,label,keyword)
        results = self.runQuery(query)

        return results


    def createIssue(self,input):
        mutation = """
          mutation{
            createIssue(input:{%s}) {
              issue{
                title
                id
              }
            }
          }
          """ % (input)
        results = self.runQuery(mutation)

        return results


    def updateIssueComment(self,commentId,newText):
        mutation = """
          mutation{
            updateIssueComment(input:{id:"%s",body:"%s"}) {
              issueComment{
                body
              }
            }
          }
          """ % (commentId,newText)
        results = self.runQuery(mutation)

        return results
    def addIssueComment(self,issueId,commentTitle):
        mutation = """
          mutation{
            addComment(input:{subjectId:"%s",body:"%s"}) {
              commentEdge{
                node{
                  body
                }
              }
            }
          }
          """ % (issueId,commentTitle)
        results = self.runQuery(mutation)

        return results


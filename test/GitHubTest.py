'''
Created on 19 Feb 2021

@author: sianob
'''
import sys
from src.GitHub import GitHub

url = str(sys.argv[1])
key = str(sys.argv[2])
org = str(sys.argv[3])
repo = str(sys.argv[4])
issueNumber = int(sys.argv[5])
issueTitle = str(sys.argv[6])

myGithub = GitHub(key)
myIssue = myGithub.getIssueByNumber(org,repo,30)

assert myIssue['data']['repository']['issue'+str(issueNumber)]['title'] == issueTitle

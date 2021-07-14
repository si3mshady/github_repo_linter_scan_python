import os, sys
import requests
import subprocess
import logging

logging.basicConfig(level = logging.ERROR, filename = 'error.log')


def remove_repo(localDirectory):
    cmd = f'rm -rf {localDirectory}'
    out, _ = execute_command(cmd)

def launchBandit(directory):
    cmd = f'bandit -r {directory}/ > {directory}.banditResults.txt'
    print(cmd)
    out, _ = execute_command(cmd)



def execute_command(cmd):
    output = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
    (out,err) = output.communicate()
    return (out,err)

def downloadRepo(repo_html):   
    cmd = f'git clone {repo_html}'
    execute_command(cmd)

def fetchPublicRepos(results,username,) -> list:
    publicRepoURL =  f"https://api.github.com/users/{username}/repos?per_page={results}"
    return  [repo['html_url'] for repo in requests.get(publicRepoURL).json()]

def init(results=0,username="si3mshady"):    
    for repo in fetchPublicRepos(results,username):
        downloadRepo(repo)
        localDirectoryName  = repo.split('/')[-1]        
        launchBandit(localDirectoryName)
        remove_repo(localDirectoryName)
        
   
if __name__ == "__main__":
    args = [val for val in sys.argv[1:]]

    if len(args) == 2:
        try:
            numOfResults = args[0]
            username = args[1]
            init(results=numOfResults, username=username)

        except Exception as e:
            logging.error(f"Exception:{e}")        

    elif len(args) == 1:
        try: 
            numOfResults = args[0]
            init(results=numOfResults)       
        #numResults username 
        except Exception as e:
            logging.error(f"Exception:{e}")        
    else:
        try:
            init()
        except Exception as e: 
            logging.error(f"Exception:{e}")     

#usage python <thisScript.py> Optional ARGS [seconds] [github_username]

#Pull Public GitHub repo & process python code for security vulns 
#Run the utility Bandit on all source code in repo
#Generate a list of vulns in python code 
# Bandit is a tool designed to find common security issues in Python code.
#To do this Bandit processes each file, builds an AST from it, and runs appropriate plugins against the #AST nodes. Once Bandit has finished scanning all the files it generates a report.
#Elliott Arnold 
#7-14-21


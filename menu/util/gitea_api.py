import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_oragnizaion(data):
    url = data["gitea_domain"]+'/api/v1/orgs'
    headers = {'Content-Type':'application/json', 'Authorization':'Basic '+data['git_cicd_auth'], 'Accept':'application/json'}
    return requests.get(url, headers=headers, verify=False).text

def get_repos_in_orgs(data):
    url = data["gitea_domain"]+'/api/v1/orgs/'+ data['organization_name']+'/repos'
    headers = {'Content-Type':'application/json', 'Authorization':'Basic '+data['git_cicd_auth'], 'Accept':'application/json'}
    return requests.get(url, headers=headers, verify=False).text

def create_oragnizaion(data):
    url = data["gitea_domain"]+'/api/v1/orgs'
    headers = {'Content-Type':'application/json', 'Authorization':'Basic '+data['git_cicd_auth'], 'Accept':'application/json'}
    payload = {
      "description": "CICD by ND",
      "email": "test@test.com",
      "full_name": data["organization_name"],
      "location": "korea",
      "username": data["organization_name"]+"-cicd",
      "visibility": "private",
      "website": "http://nnd-cicd.inje.com"
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)

def create_gitops(data):
    url = data["gitea_domain"]+'/api/v1/orgs/'+data["organization_name"]+'-cicd/repos'
    headers = {'Content-Type':'application/json', 'Authorization':'Basic '+data['git_cicd_auth'], 'Accept':'application/json'}
    payload = {
      "auto_init": True,
      "default_branch": "main",
      "license": "",
      "name": data["application_name"]+"-gitops",
      "object_format_name": "sha1",
      "private": True,
      "readme": "Default"
    }
    ## gitops
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    payload["name"] = data["application_name"]+"-dev"
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    payload["name"] = data["application_name"]+"-stg"
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    payload["name"] = data["application_name"]+"-prod"
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    ##

def create_gitea_user_id(data):
    url = data['gitea_domain'].replace("://", '://'+data["gitea_admin_id"]+':'+data["gitea_admin_pw"]+'@')+'/api/v1/admin/users'
    headers = {'Content-Type':'application/json'}
    payload = {
        "email": data['git_cicd_id']+"@cicdbot.com",
        "full_name": data['git_cicd_id'],
        "login_name": data['git_cicd_id'],
        "must_change_password": False,
        "password": data['git_cicd_pw'],
        "restricted": True,
        "send_notify": True,
        "source_id": 0,
        "username": data['git_cicd_id']
    }

    r = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
    if r.status_code == 201:
        print("Gitea Id is successfully created")
    else:
        print("create_gitea_user_id : " + str(r))

def create_gitea_oauth2(data):
    url = data['gitea_domain']+'/api/v1/admin/applications/oauth2'
    headers = {'Content-Type':'application/json', 'Authorization':'Basic '+data['git_cicd_auth']}
    payload = {
        "confidential_client": True,
        "name": "tekton-dashboard-auth200",
        "redirect_uris": [
            data['tekton_domain']+"/oauth2/callback/"
        ]
    }

    r = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
    if r.status_code == 201:
        print("Gitea oauth2 is successfully created")
    else:
        print("create_gitea_oauth2 : " + str(r))

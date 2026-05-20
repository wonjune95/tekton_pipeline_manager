import os
import json
import base64
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_registry(data):
    url = 'https://'+data["image_registry"]+'/api/v2.0/projects'
    headers = {'Content-Type':'application/json', 'Authorization':'Basic '+data['harbor_admin_auth'], 'X-Resource-Name-In-Location':'false'}
    payload= {
        "project_name": data["organization_name"],
        "public": True,
        "metadata": {
            "public": "true"
        },
        "storage_limit": -1
    }

    payload["project_name"] = data["organization_name"]+"-dev"
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    payload["project_name"] = data["organization_name"]+"-stg"
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    payload["project_name"] = data["organization_name"]+"-prod"
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)

def create_harbor_id(data):
    url = 'https://'+data['image_registry']+'/api/v2.0/users'
    headers = {'Content-Type':'application/json', 'Authorization':'Basic '+data['harbor_admin_auth'], 'X-Resource-Name-In-Location':'false'}
    payload= {
        "username": data['harbor_id'],
        "email": data['harbor_id']+"@cicdbot.com",
        "realname": data['harbor_id'],
        "password": data['harbor_pw'],
        "comment": data['harbor_id']
    }

    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    if r.status_code == 201:
        print("Harbor Id is successfully created")
    else:
        print("create_harbor_id :" + str(r))

def create_harbor_robot_id(data):
    url = 'https://'+data['image_registry']+'/api/v2.0/robots'
    headers = {'Content-Type':'application/json', 'Authorization':'Basic '+data['harbor_admin_auth'], 'X-Resource-Name-In-Location':'false'}
    payload= {
        "permissions":[
            {"kind":"project","namespace":"*","access":[{"resource":"repository","action":"push"},{"resource":"repository","action":"pull"}]}
        ]
        ,"name":data['harbor_robot_id'].split('.')[1]
        ,"description":"null"
        ,"duration":-1
        ,"disable":False
        ,"level":"system"
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)

    if r.status_code == 201:
        print("robot secret : " + r.json().get('secret'))
        data['harbor_robot_pw'] = r.json().get('secret')
        str_input = data["harbor_robot_id"]+":"+data["harbor_robot_pw"]
        str_encoded = base64.b64encode(bytes(str_input, 'UTF-8')).decode("UTF-8")
        data["harbor_robot_auth"] = str_encoded
        print("Harbor Robot Id is successfully created")
    else:
        print("create_harbor_robot_id : " + str(r))

def create_nexus_id(data):
    #url = 'https://'+data["nexus_admin_id"]+':'+data["nexus_admin_pw"]+'@'+data["nexus_host_url"]+'/service/rest/v1/security/users'
    url = data['nexus_domain'].replace("://", '://'+data["nexus_admin_id"]+':'+data["nexus_admin_pw"]+'@')+'/service/rest/v1/security/users'
    headers = {'Content-Type':'application/json'}
    payload = {
        "userId": data["nexus_id"],
        "firstName": data["nexus_id"],
        "lastName": data["nexus_id"],
        "emailAddress": "cicdbot1@cicdbot.com",
        "password": data["nexus_pw"],
        "status": "active",
        "roles": ["nx-admin"]
    }

    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    if r.status_code == 200:
        print("Nexus Id is successfully created")
    else:
        print("create_nexus_id : " + str(r))


def create_nexus_maven_repository(data):
    #url = 'https://'+data["nexus_admin_id"]+':'+data["nexus_admin_pw"]+'@'+data["nexus_host_url"]+'/service/rest/v1/repositories/maven/hosted'
    url = data['nexus_domain'].replace("://", '://'+data["nexus_admin_id"]+':'+data["nexus_admin_pw"]+'@')+'/service/rest/v1/repositories/maven/hosted'

    headers = {'Content-Type':'application/json'}
    payload = {
        "name": "maven-default",
        "online": True,
        "storage": {
            "blobStoreName": "default",
            "strictContentTypeValidation": True,
            "writePolicy": "ALLOW"
        },
        "component": {
            "proprietaryComponents": False
        },
        "maven": {
            "versionPolicy": "MIXED",
            "layoutPolicy": "STRICT",
            "contentDisposition": "INLINE"
        }
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    if r.status_code == 201:
        print("MAVEN release, snapshot repository is successfully created")
    else:
        print("create_nexus_maven_repository(deafault) : " +str(r))

    payload["name"] = "maven-default-release"
    payload["maven"]["versionPolicy"] = "RELEASE"
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    if r.status_code == 201:
        print("MAVEN release, snapshot repository is successfully created")
    else:
        print("create_nexus_maven_repository(release) : " +str(r))

    payload["name"] = "maven-default-snapshot"
    payload["maven"]["versionPolicy"] = "SNAPSHOT"
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    if r.status_code == 201:
        print("MAVEN release, snapshot repository is successfully created")
    else:
        print("create_nexus_maven_repository(snapshot) : " +str(r))
   
def create_nexus_maven_group_repository(data):
    #url = 'https://'+data["nexus_admin_id"]+':'+data["nexus_admin_pw"]+'@'+data["nexus_host_url"]+'/service/rest/v1/repositories/maven/group'
    url = data['nexus_domain'].replace("://", '://'+data["nexus_admin_id"]+':'+data["nexus_admin_pw"]+'@')+'/service/rest/v1/repositories/maven/group'

    headers = {'Content-Type':'application/json'}
    payload = {
        "name": "maven-default-group",
        "online": True,
        "storage": {
            "blobStoreName": "default",
            "strictContentTypeValidation": True
            },
        "group": {
            "memberNames": [
            "maven-default-release",
            "maven-default-snapshot",
            "maven-default",
            ]
            }
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    if r.status_code == 201:
        print("MAVEN group repository is successfully created")
    else:
        print("create_nexus_maven_group_repository(group) : " +str(r))

def create_nexus_npm_repository(data):
    #url = 'https://'+data["nexus_admin_id"]+':'+data["nexus_admin_pw"]+'@'+data["nexus_host_url"]+'/service/rest/v1/repositories/npm/hosted'
    url = data['nexus_domain'].replace("://", '://'+data["nexus_admin_id"]+':'+data["nexus_admin_pw"]+'@')+'/service/rest/v1/repositories/npm/hosted'
    headers = {'Content-Type':'application/json'}
    payload = {
        "name": "npm-default",
        "online": True,
        "storage": {
            "blobStoreName": "default",
            "strictContentTypeValidation": True,
            "writePolicy": "ALLOW"
            },
        "component": {
            "proprietaryComponents": True
            }
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    if r.status_code == 201:
        print("NPM repository is successfully created")
    else:
        print("create_nexus_npm_repository(default) : " +str(r))

def create_nexus_npm_group_repository(data):
    #url = 'https://'+data["nexus_admin_id"]+':'+data["nexus_admin_pw"]+'@'+data["nexus_host_url"]+'/service/rest/v1/repositories/npm/group'
    url = data['nexus_domain'].replace("://", '://'+data["nexus_admin_id"]+':'+data["nexus_admin_pw"]+'@')+'/service/rest/v1/repositories/npm/group'

    headers = {'Content-Type':'application/json'}
    payload = {
        "name": "npm-default-group",
        "online": True,
        "storage": {
            "blobStoreName": "default",
            "strictContentTypeValidation": True
            },
        "group": {
            "memberNames": ["npm-default"]
            }
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    if r.status_code == 201:
        print("NPM group repository is successfully created")
    else:
        print("create_nexus_npm_group_repository(group) : " +str(r))

def create_nexus_raw_repository(data):
    #url = 'https://'+data["nexus_admin_id"]+':'+data["nexus_admin_pw"]+'@'+data["nexus_host_url"]+'/service/rest/v1/repositories/raw/hosted'
    url = data['nexus_domain'].replace("://", '://'+data["nexus_admin_id"]+':'+data["nexus_admin_pw"]+'@')+'/service/rest/v1/repositories/raw/hosted'
    headers = {'Content-Type':'application/json'}
    payload = {
        "name": "raw-default",
        "online": True,
        "storage": {
            "blobStoreName": "default",
            "strictContentTypeValidation": True,
            "writePolicy": "ALLOW"
            },
            "raw": {
                "contentDisposition": "ATTACHMENT"
            }
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)

    if r.status_code == 201:
        print("RAW repository is successfully created")
    else:
        print("create_nexus_raw_repository(default) : " +str(r))

def create_nexus_raw_group_repository(data):
    #url = 'https://'+data["nexus_admin_id"]+':'+data["nexus_admin_pw"]+'@'+data["nexus_host_url"]+'/service/rest/v1/repositories/raw/group'
    url = data['nexus_domain'].replace("://", '://'+data["nexus_admin_id"]+':'+data["nexus_admin_pw"]+'@')+'/service/rest/v1/repositories/raw/group'
    headers = {'Content-Type':'application/json'}
    payload = {
        "name": "raw-default-group",
        "online": True,
        "storage": {
            "blobStoreName": "default",
            "strictContentTypeValidation": True
            },
        "group": {
            "memberNames": ["raw-default"]
            },
        "raw": {
            "contentDisposition": "ATTACHMENT"
            }
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)

    if r.status_code == 201:
        print("RAW group repository is successfully created")
    else:
        print("create_nexus_raw_group_repository(group) : " +str(r))


def create_sonar_token(data):
    url = data['sonar_domain'] +'/api/user_tokens/generate'
    sonar_admin_auth = base64.b64encode(
        f"{data['sonar_admin_id']}:{data['sonar_admin_pw']}".encode()
    ).decode()
    headers = {'Content-Type':'application/x-www-form-urlencoded', 'Authorization':'Basic ' + sonar_admin_auth}
    r = requests.post(url, headers=headers,
                      data=f"name={data['sonar_id']}&login={data['sonar_admin_id']}&type=USER_TOKEN",
                      verify=False)
    
    if r.status_code == 200:
        print("sonar_token : " + r.json().get('token'))
        data['sonar_token'] = r.json().get('token')
        print("Sonartoken is successfully created")
    else:
        print("create_sonar_token : " +str(r))

def get_organization(data):
    url = data["gitea_domain"]+'/api/v1/orgs'
    headers = {'Content-Type':'application/json', 'Authorization':'Basic '+data['git_cicd_auth'], 'Accept':'application/json'}
    r = requests.get(url, headers=headers, verify=False)
    r.raise_for_status()
    return r.text

# 하위 호환 alias (오타 버전)
get_oragnizaion = get_organization

def get_repos_in_orgs(data):
    url = data["gitea_domain"]+'/api/v1/orgs/'+ data['organization_name']+'/repos'
    headers = {'Content-Type':'application/json', 'Authorization':'Basic '+data['git_cicd_auth'], 'Accept':'application/json'}
    r = requests.get(url, headers=headers, verify=False)
    r.raise_for_status()
    return r.text

def create_organization(data):
    url = data["gitea_domain"]+'/api/v1/orgs'
    headers = {'Content-Type':'application/json', 'Authorization':'Basic '+data['git_cicd_auth'], 'Accept':'application/json'}
    payload = {
      "description": "CICD by ND",
      "email": "test@test.com",
      "full_name": data["organization_name"],
      "location": "korea",
      "username": data["organization_name"]+"-cicd",
      "visibility": "private",
      "website": "https://nnd-cicd.injeinc.com"
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)

# 하위 호환 alias (오타 버전)
create_oragnizaion = create_organization

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
    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    print("create_gitops : "+str(r))

def create_gitea_user_id(data):
    #url = 'https://'+data["gitea_admin_id"]+':'+data["gitea_admin_pw"]+'@'+data["gitea_host_url"]+'/api/v1/admin/users'
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

    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    if r.status_code == 201:
        print("Gitea Id is successfully created")
    else:
        print("create_gitea_user_id : " + str(r))

# 프로젝트별로 로그인 oauth를 생성해야 할지는 고민해봐야할 문제임...
def create_gitea_oauth2(data):
    #https://gitea.125-6-38-222.nip.io/admin/applications/oauth2
    #url = gitea_host+'/api/v1/user/applications/oauth2'
    url = data['gitea_domain']+'/api/v1/admin/applications/oauth2'
    headers = {'Content-Type':'application/json'}
    payload = {
        "confidential_client": True,
        "name": "tekton-dashboard-auth200",
        "redirect_uris": [
            data['tekton_domain']+"/oauth2/callback/"
        ]
    }

    r = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    #data['oauth_client_id'] = r.json().get('client_id')
    #data['oauth_client_secret'] = r.json().get('client_secret')

    if r.status_code == 201:
        print("Gitea oauth2 is successfully created")
    else:
        print("create_gitea_user_id : " + str(r))

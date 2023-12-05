"""
File of utility functions for the Loopio Integrations
"""
import requests
import json

HOST = "https://api.int01.loopio.com"

def __get_secrets(fn,secret) -> str: 
    """Small helper to get secrets from the file
        Inputs: 
            - filename (fn)
            - secret
        
        Returns: 
            - Value in of the secret
    """
    f = open(fn)
    dict = json.load(f)
    return dict[secret]


def get_auth_token(scope, secrets_file="./secrets/loopio_secret", ) -> str: 
    """Function to get the oauth2 bearer token from the Loopio API
    Inputs: 
        - scope: Authorization token scope (eg library:write)
        - secrets_file (optional): Location of the secrets file
    Outputs: Bearer Token (str)
    """
    host = HOST +"/oauth2/access_token"
    id = __get_secrets(secrets_file,"id")
    secret = __get_secrets(secrets_file,"secret")
    headers = {
        "content_type": "application/x-www-form-urlencoded"
    }   
    payload = { 
        "grant_type":"client_credentials", 
        "client_id":id,
        "client_secret": secret,
        "scope":scope
    }
    r = requests.post(host,headers=headers, data=payload, timeout=4)
    return r.json()["access_token"]


def get_library_entry(id=None):
    """Function to get library entries from the Loopio Library

    Inputs:
    - id (optional): The ID of a specific Loopio entry to retrieve
    """
    
    # Get the Auth Token with library:read permissions
    bearer_token = get_auth_token(scope="library:read")
    
    # Construct the URL appending the ID if provided
    url = "https://api.int01.loopio.com/data/v2/libraryEntries"
    if id is not None: 
        url = url + "/"+ str(id)

    # Construct the authorization headers and generate a request
    headers = { 
        "Accept":"application/json",
        "Authorization": "Bearer " + bearer_token
    }
    r = requests.get(url,headers=headers, timeout=10)
    return r.json()


def patch_update_library_entry(id, json_patch:list):
    """ Update a library entry
    
    Inputs: 
    - Object ID
    - json_patch: Array of JSON objects representing the patch
        Example to change the Language Code to Spanish: 
        data = [
            {"path":"/languageCode", "op":"replace", "value":"es"}
        ]
    
    """
    # Get the Bearer Token 
    bearer_token = get_auth_token(scope="library:write")

    # Construct the Request
    url = "https://api.int01.loopio.com/data/v2/libraryEntries/{id}"
    url = url.format(id=id)
    headers = {
        "Accept":"application/json",
        "Authorization": "Bearer " + bearer_token,
        "Content-Type": "application/json-patch+json",
    }

    # Execute the Patch Request 
    r = requests.patch(
        url, 
        headers=headers, 
        data=json.dumps(json_patch),
        timeout=10)
    return r.status_code
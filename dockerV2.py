import requests
import json

############  props
auth = ('user', 'password')

def catalogo(repo_url):
    url = f"{repo_url}/v2/_catalog"
    response = requests.get(url, auth=auth)
    return response.json()['repositories']

def traerTags(repo_url, img):
    url = f"{repo_url}/v2/{img}/tags/list"
    response = requests.get(url, auth=auth)
    return response.json()    

def traerManifiesto(repo_url, img, tag):
    url = f"{repo_url}/v2/{img}/manifests/{tag}"
    headers = {"Accept": "application/vnd.docker.distribution.manifest.v2+json"}
    header = requests.get(url, auth=auth, headers=headers)
    return header

def borrarManifiesto(repo_url, img, sha):
    url = f"{repo_url}/v2/{img}/manifests/{sha}"
    headers = {"Accept": "application/vnd.docker.distribution.manifest.v2+json"}
    response = requests.delete(url, auth=auth, headers=headers)
    return response
import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

token = 'REMOVED'
repo_name = 'online.lloydsbank.co.uk'

data = json.dumps({'name': repo_name, 'private': False}).encode('utf-8')
req = urllib.request.Request('https://api.github.com/user/repos', data=data, headers={
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
    'Content-Type': 'application/json'
}, method='POST')

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        res_data = json.loads(response.read())
        print(f"Repository created: {res_data['clone_url']}")
except urllib.error.HTTPError as e:
    if e.code == 422: # Already exists
        print("Repository already exists. Proceeding to push.")
    else:
        print(f"Error creating repository: {e.code} {e.reason}")
        print(e.read().decode())

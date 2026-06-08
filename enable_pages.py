import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

token = 'REMOVED'
repo = 'crowdmineinvestment/online.lloydsbank.co.uk'

# Enable GitHub Pages on main branch
data = json.dumps({
    "source": {
        "branch": "main",
        "path": "/"
    }
}).encode('utf-8')

req = urllib.request.Request(f'https://api.github.com/repos/{repo}/pages', data=data, headers={
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
    'Content-Type': 'application/json'
}, method='POST')

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        print("GitHub Pages has been enabled successfully!")
except urllib.error.HTTPError as e:
    print(f"Failed: {e.code} {e.reason}")
    print(e.read().decode())

import re

with open('C:\\Users\\xingk\\Lloyds Banking Group\\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the app-header display bug
content = content.replace(
    'style="display:none; background-color:#029352; color:white; padding:20px 30px; display:flex; align-items:center; justify-content:space-between; border-bottom:4px solid #017a44;"',
    'style="display:none; background-color:#029352; color:white; padding:20px 30px; align-items:center; justify-content:space-between; border-bottom:4px solid #017a44;"'
)

# Fix $140,000.00
content = content.replace('$140,000.00', '£140,000.00')

# Fix transactions currency from $ to £
# E.g. amount:'$40,000.00'
content = re.sub(r"amount:'\$([0-9,.]+)'", r"amount:'£\1'", content)

with open('C:\\Users\\xingk\\Lloyds Banking Group\\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

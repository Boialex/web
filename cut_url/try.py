import json

with open('url.json') as f:
    data = json.load(f)
print data
print type(data["to"])
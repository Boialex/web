import random
import string
import json
from urlparse import urlparse
from flask import request

def id_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def add_url(text):
    with open('url.json') as f:
        table = json.load(f)
    if text[0:4] != 'http':
        text = 'http://' + text
    if text in table["to"]:
        return request.url_root + table["to"][text]
    if urlparse(text).path[1:] in table["from"]:
        return None
    new_id = id_generator()
    while (new_id in table["from"]):
        new_id = id_generator()
    table["to"][text] = new_id
    table["from"][new_id] = text
    with open('url.json', 'w') as f:
        json.dump(table, f)
    return request.url_root + new_id

def find_url(some_url):
    with open('url.json') as f:
        table = json.load(f)
    print "some_url =", some_url
    if some_url in table["from"]:
        return (table["from"][some_url])
    else:
        return None
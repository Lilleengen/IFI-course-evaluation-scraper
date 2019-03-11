import re
import os
import sys
import requests
import xml.etree.ElementTree as ET

cookies = {'VRTXSSLID': sys.argv[2]}
url = 'https://www.mn.uio.no/ifi/livet-rundt-studiene/organisasjoner/fui/kursevaluering/' + sys.argv[1] +'/stats/?vrtx=feed&page='

added = 0
files = []

next_url = url
while next_url:
    r = requests.get(next_url, cookies=cookies)
    root = ET.fromstring(r.text)
    next_url = False
    root_links = root.findall('{http://www.w3.org/2005/Atom}link')
    for root_link in root_links:
        if root_link.get('rel') == 'next':
            next_url = root_link.get('href')

    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        link = entry.find('{http://www.w3.org/2005/Atom}link')
        url = link.get('href')
        if url.endswith('.json') or url.endswith('.js'):
            added += 1
            files.append(url)


if not os.path.exists(sys.argv[1]):
    os.makedirs(sys.argv[1])

for file in files:
    r = requests.get(file, cookies=cookies)

    with open(sys.argv[1] + '/' + file[file.rindex('/')+1:], 'wb') as f:
        f.write(r.content)

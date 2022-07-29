#coding: utf-8

import urllib.request
import urllib.parse
import json
import time

hist_url = "https://slack.com/api/channels.history"
delete_url = "https://slack.com/api/chat.delete"

token = 'xoxb-2974075862017-3842059675505-whqA4C5qS0hTrVsouN5NFClr'
channel = 'C02U9DNEXV1'

hist_params = {
    'channel' : channel,
    'token' : token,
    'count' : '200'
}

req = urllib.request.Request(hist_url)
hist_params = urllib.parse.urlencode(hist_params).encode('ascii')
req.data = hist_params

res = urllib.request.urlopen(req)

body = res.read()
data = json.loads(body)

for m in data['messages']:
    if (m['user'] == 'USLACKBOT'):
        print(m)
        delete_params = {
            'channel' : channel,
            'token' : token,
            'ts' :  m["ts"]
        }
        req = urllib.request.Request(delete_url)
        delete_params = urllib.parse.urlencode(delete_params).encode('ascii')
        req.data = delete_params

        res = urllib.request.urlopen(req)
        body = res.read()

        print(body)

        time.sleep(2)
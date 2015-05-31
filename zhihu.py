# -*- coding: utf-8 -*-
import requests
import json
import time
import sys
from BeautifulSoup import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'}

s = requests.Session()

'''email and password should be your own'''
s.post('http://www.zhihu.com/login',\
        data={'_xsrf':BeautifulSoup(s.get('http://www.zhihu.com/#signin').content).find(type='hidden')['value'], \
              'email':'xxx', 'password':'xxx', 'rememberme':'y'}, headers=headers)

r = s.get('http://www.zhihu.com/people/%s/followees' % sys.argv[1], headers=headers) 
html = BeautifulSoup(r.content)
followees_num = int(html.find('div',attrs={'class':'zm-profile-side-following zg-clear'}).find('a').strong.string)
count = (followees_num - 1) / 20 + 1
param =  json.loads(html.find(attrs={'class':'zh-general-list clearfix'})['data-init'])

for i in xrange(count):
    params = json.dumps({"offset":i * 20 , "order_by": "created", "hash_id": param['params']['hash_id']})
    followlist = s.post('http://www.zhihu.com/node/ProfileFolloweesListV2',\
        data={'method':'next',\
              '_xsrf':html.find(attrs={'name':'_xsrf'})['value'],\
              'params':params}, \
        headers=headers)
    followees = followlist.json()['msg']
    
    size = len(followees)
    for j in xrange(size)):
        soup = BeautifulSoup(followees[j])
        username = soup.find('a')['title']
        link = soup.find('img')['src']
        link = link[0:link.index('_')] + link[link.index('_')+2:] 
        img = s.get(link)
        f = open(username + '.jpg', 'w')
        f.write(img.content)
        f.close()
        print '%s %s download' % (username,link) 
        time.sleep(0.1)

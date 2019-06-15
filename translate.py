# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import hashlib
import time
import json

reload(sys)
sys.setdefaultencoding('utf-8')

YOUDAO_URL = 'http://openapi.youdao.com/api'
APP_KEY = '48b36bfa4499d867'
APP_SECRET = 'MuA3u7LldWpxmQmJXZenGMKIbH051gid'
ICON_DEFAULT = 'images/icon.png'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def translation(question, source='auto', to='ja'):
    # 思路是发2条request, one: 翻译成日语， two：日语翻译成中文
    items = []
    q = question.strip()

    if '' is q:
        items.append(dict(
            title='Bank', subtitle='空', icon=ICON_DEFAULT))
        return items

    curtime = str(int(time.time()))
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)

    data = {'from': source, 'to': to, 'signType': 'v3', 'curtime': curtime, 'appKey': APP_KEY, 'q': q, 'salt': salt,
            'sign': sign}

    title = q

    response = do_request(data)
    result = response.content
    reJson = json.loads(result, encoding='utf-8')  # 有个unicode坑，不知道是不是python2 的原因
    if 'translation' in reJson:
        subtitle = ''.join(reJson['translation'])
        items.append(dict(
            title=title, subtitle=subtitle, icon=ICON_DEFAULT))
    else:
        items.append(dict(
            title='Nothing', subtitle='nothing', icon=ICON_DEFAULT))
    return items


if __name__ == '__main__':
    print translation(" test")

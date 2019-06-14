from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
import sys
import uuid
import requests
import hashlib
import time
# from youdao import translation

reload(sys)
sys.setdefaultencoding('utf-8')

YOUDAO_URL = 'http://openapi.youdao.com/api'
APP_KEY = '48b36bfa4499d867'
APP_SECRET = 'MuA3u7LldWpxmQmJXZenGMKIbH051gid'

class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument() or ""
        items = []
        # results = translation(query)
        # for item in results:
        #     items.append(ExtensionResultItem(icon=item['icon'],
        #                                      name=item['title'],
        #                                      description=item['subtitle'],
        #                                      on_enter=CopyToClipboardAction(item['title'])))
        q = query

        data = {}
        data['from'] = 'auto'
        data['to'] = 'ja'
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
        sign = encrypt(signStr)
        data['appKey'] = APP_KEY
        data['q'] = q
        data['salt'] = salt
        data['sign'] = sign

        response = do_request(data)
        item.append(ExtensionResultItem(icon='images/icon.png',
                                        name=q,
                                        description='test description',
                                        on_enter=CopyToClipboardAction(response.content)))

        return RenderResultListAction(items)

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

if __name__ == '__main__':
    DemoExtension().run()
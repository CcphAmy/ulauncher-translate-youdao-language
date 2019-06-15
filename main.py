from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
import logging
from translate import translation

logger = logging.getLogger(__name__)
class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        
        items = []
        query = event.get_argument().strip() or ""

        if '' is query:
            items.append(dict(
                title='Bank', subtitle='空', icon='images/icon.png'))
            return items

        # 对字符串处理与返回
        source = extension.preferences['source'] or "auto"
        to = extension.preferences['to'] or "ja"

        results = translation(query,source,to)
        for item in results:
            items.append(ExtensionResultItem(icon=item['icon'],
                                             name=item['title'],
                                             description=item['subtitle'],
                                             on_enter=CopyToClipboardAction(item['subtitle'])))

        logger.debug(items)
        return RenderResultListAction(items)

if __name__ == '__main__':
    DemoExtension().run()
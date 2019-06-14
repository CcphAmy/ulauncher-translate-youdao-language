from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

# from youdao import translation


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

        item.append(ExtensionResultItem(icon='images/icon.png',
                                        name='test',
                                        description='test description',
                                        on_enter=CopyToClipboardAction('test')))

        return RenderResultListAction(items)

if __name__ == '__main__':
    DemoExtension().run()
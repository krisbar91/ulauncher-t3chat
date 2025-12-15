from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

import webbrowser
import urllib.parse

model_list = {
    'gemini-2.5-flash-thinking': 'Gemini 2.5 Flash (Thinking)',
    'gemini-2.5-flash': 'Gemini 2.5 Flash',
    'gemini-2.5-pro': '💎 Gemini 2.5 Pro',
    'gemini-3-pro': '💎 Gemini 3 Pro',
    'gpt-5-chat': 'ChatGPT 5',
    'gpt-5.1-thinking': '💎 ChatGPT 5 (Reasoning)',
    'gpt-5.1-instant': 'ChatGPT 5.1 (Instant)',
    'gpt-4o': 'ChatGPT 4o',
    'gpt-oss-20b': 'ChatGPT OSS 20B',
    'gpt-oss-120b': 'ChatGPT OSS 120B',
    'claude-4-sonnet': '💎 Claude 4 Sonnet',
    'claude-4-sonnet-reasoning': '💎 Claude 4 Sonnet (Reasoning)',
    'claude-4.5-haiku': 'Claude 4.5 Haiku',
    'claude-4.5-haiku-reasoning': 'Claude 4.5 Haiku (Reasoning)',
    'claude-4.5-sonnet': '💎 Claude 4.5 Sonnet',
    'claude-4.5-sonnet-reasoning': '💎 Claude 4.5 Sonnet (Reasoning)'
}

class T3Chat(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        user_arg = event.get_argument()
        option_list = []

        for i in range(6):
            model = extension.preferences[f'model_{i}']
            if model == "sep":
                if i == 0:
                    return RenderResultListAction([ExtensionResultItem(icon='images/t3_error.png',
                                                           name=f"Error: Default Slot :(",
                                                           description="Under the 'Select Model' option in settings, please ensure a seperator isn't selected.")])
                else:
                    return RenderResultListAction([ExtensionResultItem(icon='images/t3_error.png',
                                                           name=f"Error: Slot {i} :(",
                                                           description="Under the 'Select Model' option in settings, please ensure a seperator isn't selected.")])

            model_override = extension.preferences[f'model_{i}_override']
            model_display = ""

            if model_override != "":
                model = model_override
                model_display = model_override
            else:
                model_display = model_list[model]
            

            slot_name = ""
            if i == 0:
                slot_name = f"Default: {model_display}"
            else:
                slot_name = f"Slot {i}: {model_display}"

            option_list.append(ExtensionResultItem(icon='images/icon.png', name=slot_name, description=f"{user_arg}", on_enter=ExtensionCustomAction({"query": user_arg, "model": model }, keep_app_open=True)))
        return RenderResultListAction(option_list)
        """
        Due to the way Ulauncher renders entries, when trying to populate the results with all models, they clip out of the screen. For now, only five model options are provided.
        I am leaving this code here, in case things change in the future.

        for k,v in model_list.items():
            option_list.append(
                ExtensionResultItem(icon='images/icon.png', name=v, description=f"{user_arg}", on_enter=ExtensionCustomAction({"query": user_arg, "model": k }, keep_app_open=True))
            ) 
        """     
    
class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        chat_query = urllib.parse.quote_plus(data["query"])
        chat_model = data["model"]
        
        url = f"https://t3.chat/new?q={chat_query}&model={chat_model}"

        webbrowser.open(url, new=2, autoraise=True)
        return HideWindowAction()

if __name__ == '__main__':
    T3Chat().run()
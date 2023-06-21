import os

import deepl
from slack_bolt import App, Say
from slack_bolt.adapter.socket_mode import SocketModeHandler

f = open("reactionbot.txt", "r")
SLACK_BOT_TOKEN = f.read().strip('\n')
f.close()
f = open("reactionapp.txt", "r")
SLACK_APP_TOKEN = f.read().strip('\n')
f.close()

app = App(token=SLACK_BOT_TOKEN)

f = open("deepl.txt", "r")
DeepL_Key = f.read().strip('\n')
translator = deepl.Translator(DeepL_Key)
f.close()

@app.event("reaction_added")
def reaction_translate(event, say):
    replies = say.client.conversations_replies(
        channel=event["item"]["channel"], ts=event["item"]["ts"]
    )
    message = replies["messages"][0]["text"]
    reaction = event["reaction"]

    if reaction == "jp":
        target_lang = "JA"
    elif reaction == "us":
        target_lang = "EN-US"
    elif reaction == "cn":
        target_lang = "ZH"
    elif reaction == "id":
        target_lang = "ID"
    elif reaction == "fr":
        target_lang = "FR"
    elif reaction == "de":
        target_lang = "DE"
    elif reaction == "flag-id":
        target_lang = "ID"
    elif reaction == "flag-fr":
        target_lang = "FR"
    else:
        return
    result = translator.translate_text(message, target_lang=target_lang).text
    say(text=result, thread_ts=event["item"]["ts"])


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

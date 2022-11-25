import requests
import random
from datetime import date

class MyBotHandler(object):
    display_recipient: str = 'coffee-machine'

    def usage(self):
        return '''    Daily xkcd:
        This bot allow you to access to xkcd's images\n
    USAGE:
        usage: print this text
        daily: sent the daily xkct in a subject named by the today date
        get: sent the daily xkct in your subjet
        rdm: sent a random xkct in your subjet
        set:
            stream: set the default stream for the daily command
        '''

    def daily(self, bot_handler):
        xkcd_json = requests.get('https://xkcd.com/info.0.json').json()
        bot_handler.send_message(dict(
            type='stream',
            to=self.display_recipient,
            subject=date.today().strftime("%y/%m/%d"),
            content="[" + xkcd_json['alt'] + "](" + xkcd_json['img'] + ")",
        ))

    def get(self, message, bot_handler):
        xkcd_json = requests.get('https://xkcd.com/info.0.json').json()
        bot_handler.send_message(dict(
            type='stream',
            to=message['display_recipient'],
            subject=message['subject'],
            content="[" + xkcd_json['alt'] + "](" + xkcd_json['img'] + ")",
        ))

    def rdm(self, message, bot_handler):
        xkcd_json = requests.get('https://xkcd.com/info.0.json').json()
        rdm = random.randrange(0, xkcd_json['num'])
        xkcd_json = requests.get("https://xkcd.com/" + str(rdm) + "/info.0.json").json()
        bot_handler.send_message(dict(
            type='stream',
            to=message['display_recipient'],
            subject=message['subject'],
            content="[" + xkcd_json['alt'] + "](" + xkcd_json['img'] + ")",
        ))

    def set(self, words: list, message, bot_handler):
        if words[1] == "stream":
            self.display_recipient = words[2]
            bot_handler.send_message(dict(
                type='stream',
                to=message['display_recipient'],
                subject=message['subject'],
                content="The default stream has been set to \"" + self.display_recipient +"\"",
            ))


    def handle_message(self, message, bot_handler):
        if message['is_me_message'] == True:
            return
        content: str = message['content']

        if content == "usage" or content == "-h":
            bot_handler.send_message(dict(
                type='stream',
                to=message['display_recipient'],
                subject=message['subject'],
                content=self.usage(),
            ))
        if content == "get":
            self.get(message, bot_handler)
        if content == "rdm":
            self.rdm(message, bot_handler)
        if content == "daily":
            self.daily(bot_handler)
        words = content.split(' ')
        if words[0] == "set":
            self.set(words, message, bot_handler)

handler_class = MyBotHandler

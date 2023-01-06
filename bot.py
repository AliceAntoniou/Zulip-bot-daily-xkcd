import requests
import random
import time
import schedule
from datetime import date
from zulip_bots import lib

class MyBotHandler(object):
    display_recipient: str = 'coffee-machine'
    message: dict
    bot_handler: lib.ExternalBotHandler

    def send(self, content: str, to: str = None, subject: str = None):
        if to == None:
            to = self.message['display_recipient']
        if subject == None:
            subject = self.message['subject']
        self.bot_handler.send_message(dict(
            type='stream',
            to=to,
            subject=subject,
            content=content,
        ))

    def usage(self):
        return '''    Daily xkcd:
        This bot allow you to access to xkcd's images\n
    USAGE:
        usage: print this text
        daily: sent the daily xkct in a subject named by the today date
        loop: loop the bot on a daily xkcd for a specific hour
        get: sent the daily xkct in your subjet
        rdm: sent a random xkct in your subjet
        set:
            stream: set the default stream for the daily command
        '''

    def daily(self):
        xkcd_json = requests.get('https://xkcd.com/info.0.json').json()
        self.send("[" + xkcd_json['alt'] + "](" + xkcd_json['img'] + ")",
               self.display_recipient,
               subject=date.today().strftime("%y/%m/%d"))

    def loop_daily(self, words: list):
        schedule.every().day.at(words[1]).do(self.daily)
        self.send("Loop started for " + words[1])
        while (True):
            schedule.run_pending()
            time.sleep(60)

    def get(self, words: list):
        if len(words) == 1:
            xkcd_json = requests.get('https://xkcd.com/info.0.json').json()
            self.send("[" + xkcd_json['alt'] + "](" + xkcd_json['img'] + ")")
            return
        try:
            num = int(words[1])
        except:
            return
        xkcd_json = requests.get("https://xkcd.com/" + str(num) + "/info.0.json").json()
        self.send("[" + xkcd_json['alt'] + "](" + xkcd_json['img'] + ")")

    def rdm(self):
        xkcd_json = requests.get('https://xkcd.com/info.0.json').json()
        rdm = random.randrange(0, xkcd_json['num'])
        xkcd_json = requests.get("https://xkcd.com/" + str(rdm) + "/info.0.json").json()
        self.send("[" + xkcd_json['alt'] + "](" + xkcd_json['img'] + ")")

    def set(self, words: list):
        if words[1] == "stream":
            self.display_recipient = words[2]
            self.send("The default stream has been set to \"" + self.display_recipient + "\"")

    def handle_message(self, message, bot_handler):
        if message['is_me_message'] == True:
            return
        self.message = message
        self.bot_handler = bot_handler
        content: str = message['content']

        if content == "usage" or content == "-h":
            self.send(self.usage())
        if content == "rdm":
            self.rdm()
        if content == "daily":
            self.daily()
        words = content.split(' ')
        if words[0] == "loop":
            self.loop_daily(words)
        if words[0] == "get":
            self.get(words)
        if words[0] == "set":
            self.set(words)

handler_class = MyBotHandler

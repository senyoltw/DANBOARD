#!/usr/bin/env python3

"""You need to make dialogflow same name Intents.
For example :
Intent name : ifttt_remo_off
user says   : エアコン消して, エアコンをオフにして,
Responce    : わかりました。エアコンをオフにします。

Tihs is Nature Remo nad IFTTT sample.
You need buy Nature Remo http://nature.global/
"""

import subprocess

def webhook():
    ip_address = subprocess.check_output("curl -X POST https://maker.ifttt.com/trigger/remo_off/with/key/[YOUR IFTTT KEY]", shell=True, universal_newlines=True)
    word = 'エアコンをオフにしました'
    return word

if __name__ == '__main__':
    my_webhook = webhook()
    print(my_webhook)
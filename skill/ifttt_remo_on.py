#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""You need to make dialogflow same name Intents.
For example :
Intent name : ifttt_remo_on
user says   : エアコンつけて, エアコンをオンにして,
Responce    : わかりました。エアコンをオンにします。

Tihs is Nature Remo nad IFTTT sample.
You need buy Nature Remo http://nature.global/
"""

import subprocess

def webhook():
    curl_url = subprocess.check_output("curl -X POST https://maker.ifttt.com/trigger/remo_on/with/key/[YOUR IFTTT KEY]", shell=True, universal_newlines=True)
    word = 'エアコンをオンにしました'
    return word

if __name__ == '__main__':
    my_webhook = webhook()
    print(my_webhook)
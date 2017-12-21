#!/usr/bin/env python3

"""You need to make dialogflow same name Intents.
For example :
Intent name : myip
user says   : Say your ip, Check ip address,
Responce    : OK. Check My ip address
"""

import subprocess

def MyIP():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True, universal_newlines=True)
    word = '私のIPアドレスは' + ip_address.replace("\n", "") + 'です'
    return word

if __name__ == '__main__':
    IP = MyIP()
    print(IP)
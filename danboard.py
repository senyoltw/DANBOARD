#!/usr/bin/env python3

import aiy.audio
import aiy.cloudspeech
import aiy.i18n
import aiy.voicehat

import mod.snowboydecoder as snowboydecoder
import mod.detect_intent_texts as detect_intent_texts
import mod.tts_jp as tts
import mod.skill  as skill

import os
import sys
import uuid
import subprocess

aiy.i18n.set_language_code('ja-JP')
myuuid = str(uuid.uuid4())
model = os.path.join(os.path.dirname(__file__),'danbo-.pmdl')

def callbacks():
    #snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def main():
    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
    recognizer = aiy.cloudspeech.get_recognizer()
    text_recognizer = detect_intent_texts.get_recognizer()
    status_ui = aiy.voicehat.get_status_ui()
    aiy.audio.get_recorder().start()

    while True:
        print('INFO:Speak Wake Word and speak')
        status_ui.status('ready')

        global interrupted
        interrupted = False

        detector.start(detected_callback=callbacks,
                       interrupt_check=interrupt_callback,
                       sleep_time=0.03)

        print('INFO:Listening...')
        status_ui.status('thinking')
        text = recognizer.recognize()

        if not text:
            print('INFO:Sorry, I did not hear you.')
        else:
            print('INFO:"', text, '"')
            answer = text_recognizer.recognize(myuuid, text)
            if answer.intent.display_name == "Default Fallback Intent":
                print('INFO:Sorry, Unrecognized text.')
            else:
                tts.say(answer.fulfillment_text)

                while answer.all_required_params_present == False:
                    print('INFO:You speak more params')
                    text_params = recognizer.recognize()
                    answer = text_recognizer.recognize(myuuid, text_params)
                    tts.say(answer.fulfillment_text)

                skill_result = skill.execution(answer.intent.display_name)
                if not skill_result is None:
                    print(skill_result)
                    tts.say(skill_result)

if __name__ == '__main__':
    main()

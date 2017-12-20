#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google CloudSpeech recognizer."""

import aiy.audio
import aiy.cloudspeech
import aiy.i18n

import mod.snowboydecoder as snowboydecoder
import mod.detect_intent_texts as detect_intent_texts
import mod.tts_jp as tts

import os
import sys
import uuid

aiy.i18n.set_language_code('ja-JP')

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

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
    aiy.audio.get_recorder().start()

    while True:
        print('INFO:Speak Wake Word and speak')

        global interrupted
        interrupted = False

        detector.start(detected_callback=callbacks,
                       interrupt_check=interrupt_callback,
                       sleep_time=0.03)

        print('INFO:Listening...')
        text = recognizer.recognize()

        if not text:
            print('INFO:Sorry, I did not hear you.')
        else:
            print('INFO:"', text, '"')
            answer = text_recognizer.recognize(str(uuid.uuid4()),text).fulfillment_text
            tts.say(answer)

if __name__ == '__main__':
    main()

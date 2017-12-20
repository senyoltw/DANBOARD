#!/bin/bash

install_dir=~/voice-recognizer-raspi/src/

if [ ! -e $install_dir ]
then
  echo $install_dir not found
  echo You need install aiyprojects-raspbian
  echo How to install https://github.com/google/aiyprojects-raspbian/blob/voicekit/HACKING.md
  exit 1
fi

## COPY FILE
git ls-files | rsync -av   --exclude=".*" \
                           --exclude="LICENSE" \
                           --exclude="README.md" \
                           --exclude="install.sh" \
                           --files-from - . $install_dir


## INSTALL dialogflow
cd ~/voice-recognizer-raspi/
env/bin/pip install dialogflow

## FOR "ImportError: cannot import name 'opentype'"
env/bin/pip install --upgrade google-auth-oauthlib

## INSTALL Open JTalk
echo "Would you like to install Open JTalk(for Japanese) ?[y/n]"
read ANSWER

case $ANSWER in
    [yY] )
        sudo apt-get install open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001;;
    * )
        echo "OK. I don't install Open JTalk";;
esac
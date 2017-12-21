#!/bin/bash

## CHECK AIY-projects path
install_dir=~/AIY-projects-python/src/

if [ ! -e $install_dir ]
then
  echo $install_dir not found
  echo "You need install aiyprojects-raspbian"
  echo "How to install https://github.com/google/aiyprojects-raspbian/blob/voicekit/HACKING.md"
  echo "...or fix this script"
  exit 1
fi

## COPY FILE
echo "Install DANBOARD to AIY-projects."
git ls-files | rsync -av   --exclude=".*" \
                           --exclude="LICENSE" \
                           --exclude="README.md" \
                           --exclude="install.sh" \
                           --files-from - . $install_dir


## INSTALL dialogflow
echo "Install dialogflow Python module."
cd ~/voice-recognizer-raspi/
env/bin/pip install dialogflow

## FOR "ImportError: cannot import name 'opentype'"
echo "Upgrade google-auth-oauthlib."
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
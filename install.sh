#!/bin/bash

## CHECK AIY-projects path
install_dir_1=~/AIY-projects-python
install_dir_2=~/voice-recognizer-raspi

if [ -e $install_dir_1 ]
then
  install_dir = install_dir_1
  echo $install_dir_1 found
elif [ -e $install_dir_2 ]
then
  install_dir = install_dir_2
  echo $install_dir_2 found
else
  echo "aiyprojects-raspbian install dir not found"
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
                           --files-from - . $install_dir/src

## INSTALL snowboy need lib
echo "Install snowboy need lib."
sudo apt-get install libatlas-base-dev

## INSTALL dialogflow
echo "Install dialogflow Python module."
cd $install_dir
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
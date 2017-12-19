#!/bin/bash

install_dir=~/voice-recognizer-raspi/src/

if [ ! -e $install_dir ]
then
  echo $install_dir not found
  echo You need install aiyprojects-raspbian
  echo How to install https://github.com/google/aiyprojects-raspbian/blob/voicekit/HACKING.md
  exit 1
fi

git ls-files | rsync -av   --exclude=".*" \
                           --exclude="LICENSE" \
                           --exclude="README.md" \
                           --exclude="install.sh" \
                           --files-from - . $install_dir

#!/usr/bin/env python3

"""Wrapper around a open jtalk system."""

import logging
import os
import subprocess
import tempfile
import aiy.audio

TMP_DIR = '/run/user/%d' % os.getuid()
voice = '/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice'

def say(words, voice=voice,  player=aiy.audio.get_player()):
    """Say the given words with TTS.
    Args:
      player: To play the text-to-speech audio.
      words: string to say aloud.
    """
    try:
        (fd, tts_wav) = tempfile.mkstemp(suffix='.wav', dir=TMP_DIR)
    except IOError:
        logger.exception('Using fallback directory for TTS_JP output')
        (fd, tts_wav) = tempfile.mkstemp(suffix='.wav')
    os.close(fd)

    dic   = '/var/lib/mecab/dic/open-jtalk/naist-jdic'
    #voice = '/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice'
    speed = '1.3'

    try:
        c = subprocess.Popen(['open_jtalk', '-x', dic, '-m', voice, '-ow', tts_wav, '-r', str(speed)], stdin=subprocess.PIPE)
        c.stdin.write(words.encode())
        c.stdin.close()
        c.wait()
        player.play_wav(tts_wav)
    finally:
        os.unlink(tts_wav)



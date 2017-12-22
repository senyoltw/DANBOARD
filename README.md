# DANBOARD
DANBOARD is module. Add Dialogflow and Snowboy API for AIY Voice Kit

# How to use
You need to install aiyprojects-raspbian before install DANBOARD.  
Install aiyprojects-raspbian for reference.
https://github.com/google/aiyprojects-raspbian/blob/aiyprojects/HACKING.md

Then execute the following command

```
# git clone https://github.com/senyoltw/DANBOARD
# cd DANBOARD
# sh install.sh
```
You can use Dialogflow and Snowboy API on Voice Kit.  
And You can run any script with the same name as dialogflow intent names.

# Description demo app 
- snowboy_demo.py  
 snowboy -> Cloud Speech ->  print  text
 
 - dialogflow_audio_demo.py  
 snowboy ->  dialogflow(audio) -> print dialogflow recognize text
 
 - dialogflow_text_demo.py  
 snowboy -> Cloud Speech -> dialogflow(text) -> print dialogflow recognize text
 
 # Description mod
- detect_intent_stream.py  
DialogFlow API Detect Intent from an audio stream.  
How to use it -> see dialogflow_audio_demo.py  

- detect_intent_texts.py  
DialogFlow API Detect Intent from text inputs.  
How to use it -> see dialogflow_text_demo.py  

- skill.py  
RUN any script with the same name as dialogflow intent names.  
How to use it -> see danboard.py  

- snowboydecoder.py  
DNN based hotword and wake word detection API.  
How to use it -> see snowboy_demo.py  

- tts_jp.py  
にほんごしゃべるやつ  
How to use it -> see danboard.py  

#!/usr/bin/env python3

import os
import subprocess

def execution(skill_name):
    skill_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'skill', skill_name) + '.py'
    if os.path.exists(skill_path) == True:
       print('Skill', skill_path, 'found!')
       print('Skill execution start!')
       result = subprocess.check_output(['python', skill_path], universal_newlines=True)
       print('Skill execution end!')
       return result
    else:
       return None
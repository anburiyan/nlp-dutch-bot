# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 23:46:27 2018

@author: anburiyan
"""

from flask import Flask
from web.talk import talk

app = Flask(__name__)
app.register_blueprint(talk)
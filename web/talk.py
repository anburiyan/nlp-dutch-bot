# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 23:46:27 2018

@author: anburiyan
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

"""
Boot dutch for you 
"""

from flask import Flask, Blueprint
from flask import render_template, jsonify, request
import requests
import utils.util as u
import brain.conversations as con
import logging

logger = logging.getLogger(__name__)

talk = Blueprint("talk", __name__)


@talk.route('/')
def hello_world():
    """
    Sample hello world
    """
    return render_template('home.html')


@talk.route('/talk_todutch', methods=["POST"])
def talk_todutch():
    """ Talk with your dutch whatever you need. She can respond you whatever she knows """
    output = ''
    try:
        logger.info("Calling talk to dutch")
        user_input = request.form["text"]
        user_input = u.clean_input(user_input)
        # get unique id of who connected with dutch and the dutch brain unique id
        output = con.find_on_memory(user_input, "abcd1234", 'abcd123456789')        
    except Exception as exp:
        logger.error(
            "Error is occured while finding on memeory {0}".format(exp))
        output = "Sorry I am not trained to do that yet..."
    return jsonify({"status": "success", "response": output})

# talk.config["DEBUG"] = True
# if __name__ == "__main__":
#     talk.run(port=8000)

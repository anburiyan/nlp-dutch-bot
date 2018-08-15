# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 23:46:27 2018

@author: anburiyan
"""
#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from web import app
import logging
import os
import time

logfilepath = os.path.abspath(os.path.join(
    os.path.abspath(__name__), os.pardir))+"/logs/"
if not os.path.exists(logfilepath):
    os.mkdir(logfilepath)
logfilepath = "{0}{1}_log.log".format(logfilepath, time.strftime("%Y%d%d"))
logging.basicConfig(filename=logfilepath,level="ERROR")

logger = logging.getLogger(__name__)

app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8000)
    logger.info('Started http server on port %s' % 8000)

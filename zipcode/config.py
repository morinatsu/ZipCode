#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import os.path

# configuration
(DIRNAME, dummy) = os.path.split(os.path.dirname(__file__))
DATABASE = os.path.join(DIRNAME,'db','zip_db')
TESTING = True
DEBUG = True

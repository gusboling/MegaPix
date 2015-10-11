import webapp2
import cgi
import os
import datetime
import logging
import json
import time

from google.appengine.api import users 
from google.appengine.ext import ndb

class movie(ndb.Model):
	title = ndb.StringProperty()
	year = ndb.IntegerProperty()
	rt_rat = ndb.IntegerProperty()
	runtime = ndb.StringProperty()
	plot = ndb.StringProperty()
	poster_url = ndb.StringProperty()


class user(ndb.Model):
	name = ndb.StringProperty()
	picks = ndb.KeyProperty(repeated=True, kind=movie)
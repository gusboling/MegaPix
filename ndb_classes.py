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
	title=ndb.StringProperty()
	year=ndb.IntegerProperty()
	rated=ndb.StringProperty()
	runtime=ndb.StringProperty()
	plot=ndb.StringProperty()
	genre=ndb.StringProperty()
	director=ndb.StringProperty()
	poster_url=ndb.StringProperty()
	actors=ndb.StringProperty()
	awards=ndb.StringProperty()
	imdbrat=ndb.FloatProperty()



	@staticmethod
	def get_by_title(title):
		return movie.query(movie.title == title).get()

class user(ndb.Model):
	name = ndb.StringProperty(indexed=True)
	picks = ndb.KeyProperty(repeated=True, kind=movie)
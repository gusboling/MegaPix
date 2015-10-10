#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import requests
import cgi
import os
import logging
import json
import jinja2

from google.appengine.ext import ndb
from ndb_classes import movie

jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('control_panel.html')

        num_mov = movie.query(movie.title != "").count()

        template_values = {
        'num_mov':num_mov,
        }

        self.response.out.write(template.render(template_values))

class GetTitles(webapp2.RequestHandler):
    umovpar = movie(id="umovpar")
    def get(self):
        json_movies = open('json_movies.txt', 'r')
        for line in json_movies:
            json_line = json.loads(line)
            new_entity = movie(
                runtime=json_line['runtime'],
                plot=json_line['plot'],
                poster_url=json_line['poster_url'],
                title=json_line['title'],
                id=json_line['title'],
                parent=ndb.Key(movie,"umovpar")
                )
            fyear = json_line['year'][0]+json_line['year'][1]+json_line['year'][2]+json_line['year'][3] #Horrible hack to get around UTF8 wierdness...
            new_entity.year = int(fyear)
            if json_line['rt_rat'] != 'N/A':
                new_entity.rt_rat = int(json_line['rt_rat'])
            if len(movie.query(movie.title==new_entity.title).fetch()) == 0:
                new_entity.put()
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/get_titles', GetTitles)
], debug=True)

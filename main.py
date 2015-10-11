
import webapp2
import requests
import cgi
import os
import logging
import json
import jinja2

from google.appengine.ext import ndb
from ndb_classes import movie
from ndb_classes import user

jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

class HomePage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<h1>Hello World</h1><a href="/cp"><h3> I\'m a placeholder!</h3></a>')

class UpdateMovies(webapp2.RequestHandler):
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
            if len(movie.query(movie.title==new_entity.title).fetch()) == 0: #No matching entities in datastore. Prevents repeat entries.
                new_entity.put()
        self.redirect('/')

class ControlPanel(webapp2.RequestHandler):
    def get(self):
        template=jinja_environment.get_template('control_panel.html')
        
        num_mov = movie.query(movie.title != "").count()
        num_use = user.query().count()

        template_values = {
        'num_mov':num_mov,
        'num_use':num_use
        }

        self.response.out.write(template.render(template_values))

class UpdateUser(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = jinja_environment.get_template('create_user.html')
        self.response.out.write(template.render(template_values))
    def post(self):
        temp_user = user(id=self.request.get('name'))
        temp_user.name = self.request.get('name')
        mov_name = self.request.get('pick0')
        temp_user.picks = [ndb.Key(movie, self.request.get('pick0')), ndb.Key(movie,self.request.get('pick1')) , ndb.Key(movie,self.request.get('pick2'))]

        temp_user.put()

        self.redirect('/cp')

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/cp', ControlPanel),
    ('/update_movies', UpdateMovies),
    ('/update_user', UpdateUser)
], debug=True)

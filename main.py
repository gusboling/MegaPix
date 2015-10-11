
import webapp2
import cgi
import os
import logging
import json
import jinja2

from google.appengine.ext import ndb

from ndb_classes import movie
from ndb_classes import user

jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))


class ControlPanel(webapp2.RequestHandler):
    def get(self):
        template=jinja_environment.get_template('control_panel.html')
        
        num_mov = movie.query().count()
        num_use = user.query().count()

        movie_object = movie.get_by_title("Captain America: The Winter Soldier");

        template_values = {
        'num_mov':num_mov,
        'num_use':num_use
        }

        self.response.out.write(template.render(template_values))

class SignUp(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/html/signup.html')
        template_values = {}
        self.response.out.write(template.render(template_values))

class HomePage(webapp2.RequestHandler):
    def get(self):
        pass

class UpdateMovies(webapp2.RequestHandler):
    umovpar = movie(id="umovpar")
    def get(self):
        json_movies = open('json_movies.txt', 'r')
        for line in json_movies:
            json_line = json.loads(line)
            new_entity = movie(
                    title=json_line['title'],
                    rated=json_line['year'],
                    runtime=json_line['runtime'],
                    plot=json_line['plot'],
                    genre=json_line['genre'],
                    director=json_line['director'],
                    actors=json_line['actors'],
                    awards=json_line['awards'],
                    poster_url=json_line['poster_url']

                )
            fyear = json_line['year'][0]+json_line['year'][1]+json_line['year'][2]+json_line['year'][3] #Horrible hack to get around UTF8 wierdness...
            new_entity.year = int(fyear)
            if json_line['imdbrat'] != 'N/A':
                new_entity.imdbrat = float(json_line['imdbrat'])
            if len(movie.query(movie.title==new_entity.title).fetch()) == 0: #No matching entities in datastore. Prevents repeat entries.
                new_entity.put()
        self.redirect('/')

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

        self.redirect('/home')

class ClearMovies(webapp2.RequestHandler):
    def get(self): 
        movie_list = movie.query().fetch(500)
        for mov in movie_list:
            mov.key.delete()

app = webapp2.WSGIApplication([
    ('/', SignUp),
    ('/cp', ControlPanel),
    ('/clearmovies', ClearMovies),
    ('/home', HomePage),
    ('/update_movies', UpdateMovies),
    ('/update_user', UpdateUser)
], debug=True)



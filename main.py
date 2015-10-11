
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

class ClearMovies(webapp2.RequestHandler):
    def get(self): 
        movie_list = movie.query().fetch(500)
        for mov in movie_list:
            mov.key.delete()

class Search(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/html/intial_search.html')
        template_values={}
        self.response.out.write(template.render(template_values))

    def post(self):
        t_title = self.request.get('title') #DEFAULT VALUE IS "default_value"
        #t_genre = self.request.get('genre') #DOESN'T CURRENTLY WORK...
        t_year = int(self.request.get('year')) #DEFAULT VALUE IS 0
        t_rating = int(self.request.get('rating'))#DEFAULT VALUE IS 0

        if t_title == "default_value":
            if t_year != 0:
                result_list = movie.query(movie.year == t_year, movie.rt_rating >= t_rating).fetch(200)
            else:
                result_list = movie.query(movie.rt_rating >= t_rating).fetch()
        else:
            if t_year != 0:
                result_list = movie.query(movie.title == t_title, movie.year == t_year, movie.imdbrat >= t_rating).fetch()
            elif t_rating != 0:
                result_list = movie.query(movie.title == t_title, movie.rt_rating >= t_rating).fetch()
            else:
                result_list = movie.query().fetch()

        template_values = {
            'result_list': result_list
        }

        template = jinja_environment.get_template('/html/search.html')
        self.response.out.write(template.render(template_values))

class HomePage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/html/index.html')
        result_list = movie.query(movie.rt_rating >= 80).fetch(20)
        template_values = {
        'result_list':result_list
        }
        self.response.out.write(template.render(template_values))

class SignUp(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/html/signup.html')
        template_values = {}
        self.response.out.write(template.render(template_values))

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
            if json_line['rt_rating'] != 'N/A':
                new_entity.rt_rating = int(json_line['rt_rating'])
            if len(movie.query(movie.title==new_entity.title).fetch()) == 0: #No matching entities in datastore. Prevents repeat entries.
                new_entity.put()
        self.redirect('/home')

class UpdateUser(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = jinja_environment.get_template('create_user.html')
        self.response.out.write(template.render(template_values))
    def post(self):
        temp_user = user(id=self.request.get('name'))
        temp_user.name = self.request.get('name')
        temp_user.put()
        self.redirect('/home')


app = webapp2.WSGIApplication([
    ('/', SignUp),
    ('/home', HomePage),
    ('/search', Search),
    ('/updatemovies', UpdateMovies),
    ('/clearmovies', ClearMovies),
    ('/home', HomePage),
    ('/update_movies', UpdateMovies),
    ('/update_user', UpdateUser)
], debug=True)



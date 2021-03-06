#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
from datetime import datetime
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Show(db.Model):
  __tablename__ = 'Show'

  start_time = db.Column('start_time',db.DateTime, primary_key = True)
  artist_id = db.Column('artist_id',db.Integer, db.ForeignKey('Artist.id'))
  venue_id = db.Column('venue_id',db.Integer, db.ForeignKey('Venue.id'))
#  venue = db.relationship('Venue', backref=db.backref('shows', lazy=True))
#  artist = db.relationship('Artist', backref=db.backref('shows', lazy=True))
  def __repr__(self):
    return '<Show with Artist {} and Venue {} at {}>'.format(self.artist_id, self.venue_id, self.start_time)



class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String())
    website = db.Column(db.String(255))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean,default=False)
    seeking_description = db.Column(db.String())
    shows = db.relationship('Show', lazy=True, backref=db.backref('venue', lazy=True))

    def __repr__(self):
      return '<Venue {} id: {}, city: {}, state: {}, address: {}, phone: {}>'.format(self.name, self.id, self.city, self.state, self.address, self.phone)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(255))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())
    shows = db.relationship('Show', lazy=True, backref=db.backref('artist', lazy=True))

    def __repr__(self):
      return """<Artist {} 
                  id:{}, city:{}, state:{}, 
                  phone: {}, genres: {}, website: {}, 
                  image_link: {}, facebook_link: {}, 
                  seeking_venue: {}, seeking_description: {}
                  >""".format(self.name, 
                              self.id, self.city, self.state, 
                              self.phone, self.genres, self.website,
                              self.image_link, self.facebook_link,
                              self.seeking_venue, self.seeking_description)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  venues = Venue.query.order_by('city', 'state').all()
  cities = {}

  for venue in venues:
    city = '{}, {}'.format(venue.city, venue.state)
    if not city in cities:
      cities[city] = {'city': venue.city, 'state': venue.state, 'venues': []}
    cities[city]['venues'].append({'id': venue.id,
                                   'name': venue.name,
                                   'num_upcoming_shows': 
                                    len(
                                      list(
                                        filter(
                                          lambda s: s.start_time > datetime.today() , venue.shows
                                        )
                                      )
                                    )})
                                    
  data = []
  for city in cities:
    data.append(cities[city])

#  print(data)
  
#  data=[{
#    "city": "San Francisco",
#    "state": "CA",
#    "venues": [{
#      "id": 1,
#      "name": "The Musical Hop",
#      "num_upcoming_shows": 0,
#    }, {
#      "id": 3,
#      "name": "Park Square Live Music & Coffee",
#      "num_upcoming_shows": 1,
#    }]
#  }, {
#    "city": "New York",
#    "state": "NY",
#    "venues": [{
#      "id": 2,
#      "name": "The Dueling Pianos Bar",
#      "num_upcoming_shows": 0,
#    }]
#  }]
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_term=request.form.get('search_term')

  venues = Venue.query.filter(Venue.name.ilike('%{}%'.format(search_term))).all()

  response={
    "count": len(venues),
    "data": []
  }

  for venue in venues:
    response["data"].append(
      {
        "id": venue.id, 
        "name": venue.name, 
        "num_upcoming_shows": len(
          list(
            filter(
              lambda s: s.start_time > datetime.today(), 
              venue.shows
            )
          )
        )
      }
    )
  
 # response={
 #   "count": 1,
 #   "data": [{
 #     "id": 2,
 #     "name": "The Dueling Pianos Bar",
 #     "num_upcoming_shows": 0,
 #   }]
 # }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  venue = Venue.query.get(venue_id)

  if venue is None:
    flash('Venue with ID {} not found!'.format(venue_id))
    return redirect(url_for('index'))
  else:
    upcoming_shows = list(filter(lambda s: s.start_time > datetime.today() , venue.shows))
    past_shows = list(filter(lambda s: s.start_time <= datetime.today() , venue.shows))
    data={
     "id": venue.id,
     "name": venue.name,
      "genres": venue.genres.split(','),
      "city":venue.city,
      "phone":venue.phone,
      "address": venue.address,
      "website": venue.website,
     "facebook_link": venue.facebook_link,
     "seeking_talent": venue.seeking_talent,
     "seeking_description": venue.seeking_description,
     "image_link": venue.image_link,
     "past_shows": [{"artist_id": s.artist_id,
                     "artist_name": s.artist.name,
                     "artist_image_link": s.artist.image_link,
                     "start_time": s.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")} for s in past_shows],
     "upcoming_shows": [{"artist_id": s.artist_id,
                     "artist_name": s.artist.name,
                     "artist_image_link": s.artist.image_link,
                     "start_time": s.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")} for s in upcoming_shows],
     "past_shows_count": len(past_shows),
     "upcoming_shows_count": len(upcoming_shows),
   }
  
#  data1={
#    "id": 1,
#    "name": "The Musical Hop",
#    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
#    "address": "1015 Folsom Street",
#    "city": "San Francisco",
#    "state": "CA",
#    "phone": "123-123-1234",
#    "website": "https://www.themusicalhop.com",
#    "facebook_link": "https://www.facebook.com/TheMusicalHop",
#    "seeking_talent": True,
#    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
#    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
#    "past_shows": [{
#      "artist_id": 4,
#      "artist_name": "Guns N Petals",
#      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#      "start_time": "2019-05-21T21:30:00.000Z"
#    }],
#    "upcoming_shows": [],
#    "past_shows_count": 1,
#    "upcoming_shows_count": 0,
#  }
#  data2={
#    "id": 2,
#    "name": "The Dueling Pianos Bar",
#    "genres": ["Classical", "R&B", "Hip-Hop"],
#    "address": "335 Delancey Street",
#    "city": "New York",
#    "state": "NY",
#    "phone": "914-003-1132",
#    "website": "https://www.theduelingpianos.com",
#    "facebook_link": "https://www.facebook.com/theduelingpianos",
#    "seeking_talent": False,
#    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
#    "past_shows": [],
#    "upcoming_shows": [],
#    "past_shows_count": 0,
#    "upcoming_shows_count": 0,
#  }
#  data3={
#    "id": 3,
#    "name": "Park Square Live Music & Coffee",
#    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
#    "address": "34 Whiskey Moore Ave",
#    "city": "San Francisco",
#    "state": "CA",
#    "phone": "415-000-1234",
#    "website": "https://www.parksquarelivemusicandcoffee.com",
#    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
#    "seeking_talent": False,
#    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#    "past_shows": [{
#      "artist_id": 5,
#      "artist_name": "Matt Quevedo",
#      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
#      "start_time": "2019-06-15T23:00:00.000Z"
#    }],
#    "upcoming_shows": [{
#      "artist_id": 6,
#      "artist_name": "The Wild Sax Band",
#      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#      "start_time": "2035-04-01T20:00:00.000Z"
#    }, {
#      "artist_id": 6,
#      "artist_name": "The Wild Sax Band",
#      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#      "start_time": "2035-04-08T20:00:00.000Z"
#    }, {
#      "artist_id": 6,
#      "artist_name": "The Wild Sax Band",
#      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#      "start_time": "2035-04-15T20:00:00.000Z"
#    }],
#    "past_shows_count": 1,
#    "upcoming_shows_count": 1,
#  }
#  data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  data = request.form
  error = False
  #print(request.form)

  try:
    venue = Venue(
      name=request.form.get('name'),
      city=request.form.get('city'),
      state=request.form.get('state'),
      address=request.form.get('address'),
      genres=','.join(request.form.getlist('genres')),
      phone=request.form.get('phone'),
      image_link=request.form.get('image_link'),
      facebook_link=request.form.get('facebook_link'),
      website=request.form.get('website'),
      seeking_talent=(request.form.get('seeking_talent')=='y'),
      seeking_description=request.form.get('seeking_description')
    )
  
    db.session.add(venue)
    db.session.commit()
    data = venue
  except:
    db.session.rollback()
    error=True
  finally:
    db.session.close()

  # on successful db insert, flash success
  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('An error occurred. Venue {} could not be created.'.format(request.form['name']))
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():

  artists = Artist.query.all()
  # TODO: replace with real data returned from querying the database

#  data=[{
#    "id": 4,
#    "name": "Guns N Petals",
#  }, {
#    "id": 5,
#    "name": "Matt Quevedo",
#  }, {
#    "id": 6,
#    "name": "The Wild Sax Band",
#  }]
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term=request.form.get('search_term')

  artists = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).all()
  data = []
  for artist in artists:

    data.append({"id": artist.id, "name": artist.name, "num_upcoming_shows": len(list(filter(lambda s: s.start_time > datetime.today(), artist.shows)))})
  response={
    "count": len(artists),
    "data": data
    #[{
    #  "id": 4,
    #  "name": "Guns N Petals",
    #  "num_upcoming_shows": 0,
    #}]


  }
  print(response)
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  artist = Artist.query.get(artist_id)
  upcoming_shows = list(filter(lambda s: s.start_time > datetime.today(), artist.shows))
  past_shows = list(filter(lambda s: s.start_time <= datetime.today(), artist.shows))
  print(artist)
  if artist is None:
    flash('Artist with ID {} not found'.format(artist_id))
    redirect(url_for('index'))
  else:
    data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres.split(','),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": [{"venue_id": s.venue_id,
                    "venue_name": s.venue.name,
                    "venue_image_link": s.venue.image_link, 
                    "start_time": s.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")} for s in past_shows],
    "upcoming_shows": [{"venue_id": s.venue_id,
                        "venue_name": s.venue.name,
                        "venue_image_link": s.venue.image_link, 
                        "start_time": s.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")} for s in upcoming_shows],
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
    }

#  data1={
#    "id": 4,
#    "name": "Guns N Petals",
#    "genres": ["Rock n Roll"],
#    "city": "San Francisco",
#    "state": "CA",
#    "phone": "326-123-5000",
#    "website": "https://www.gunsnpetalsband.com",
#    "facebook_link": "https://www.facebook.com/GunsNPetals",
#    "seeking_venue": True,
#    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
#    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#    "past_shows": [{
#      "venue_id": 1,
#      "venue_name": "The Musical Hop",
#      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
#      "start_time": "2019-05-21T21:30:00.000Z"
#    }],
#    "upcoming_shows": [],
#    "past_shows_count": 1,
#    "upcoming_shows_count": 0,
#  }
#  data2={
#    "id": 5,
#    "name": "Matt Quevedo",
#    "genres": ["Jazz"],
#    "city": "New York",
#    "state": "NY",
#    "phone": "300-400-5000",
#    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
#    "seeking_venue": False,
#    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
#    "past_shows": [{
#      "venue_id": 3,
#      "venue_name": "Park Square Live Music & Coffee",
#      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#      "start_time": "2019-06-15T23:00:00.000Z"
#    }],
#    "upcoming_shows": [],
#    "past_shows_count": 1,
#    "upcoming_shows_count": 0,
#  }
#  data3={
#    "id": 6,
#    "name": "The Wild Sax Band",
#    "genres": ["Jazz", "Classical"],
#    "city": "San Francisco",
#    "state": "CA",
#    "phone": "432-325-5432",
#    "seeking_venue": False,
#    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#    "past_shows": [],
#    "upcoming_shows": [{
#      "venue_id": 3,
#      "venue_name": "Park Square Live Music & Coffee",
#      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#      "start_time": "2035-04-01T20:00:00.000Z"
#    }, {
#      "venue_id": 3,
#      "venue_name": "Park Square Live Music & Coffee",
#      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#      "start_time": "2035-04-08T20:00:00.000Z"
#    }, {
#      "venue_id": 3,
#      "venue_name": "Park Square Live Music & Coffee",
#      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#      "start_time": "2035-04-15T20:00:00.000Z"
#    }],
#    "past_shows_count": 0,
#    "upcoming_shows_count": 3,
#  }
 # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  artist.genres = artist.genres.split(',')
  form = ArtistForm(obj=artist)
  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  print(request.form)
  artist = Artist.query.get(artist_id)
  error = False
  artist.name = request.form.get('name')
  artist.genres = ','.join(request.form.getlist("genres"))
  artist.city = request.form.get("city")
  artist.state = request.form.get("state")
  artist.phone = request.form.get("phone")
  artist.website = request.form.get("website")
  artist.facebook_link = request.form.get("facebook_link")
  artist.seeking_venue = (request.form.get("seeking_venue") == 'y')
  artist.seeking_description = request.form.get("seeking_description")
  artist.image_link = request.form.get("image_link")
  
  print(artist)

  try:
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    flash('Artist {} could not be edited'.format(artist_id))
  else:
    flash('Artist {} successfully edited'.format(artist_id))
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  
  venue = Venue.query.get(venue_id)
  venue.genres = venue.genres.split(',')
  form = VenueForm(obj=venue)
#  venue={
#    "id": 1,
#    "name": "The Musical Hop",
#    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
#    "address": "1015 Folsom Street",
#    "city": "San Francisco",
#    "state": "CA",
#    "phone": "123-123-1234",
#    "website": "https://www.themusicalhop.com",
#    "facebook_link": "https://www.facebook.com/TheMusicalHop",
#    "seeking_talent": True,
#    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
#    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
 # }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  print(request.form.get("seeking_talent"))
  venue = Venue.query.get(venue_id)
  venue.name = request.form.get("name")
  venue.genres = ','.join(request.form.getlist("genres"))
  venue.address = request.form.get("address")
  venue.city = request.form.get("city")
  venue.state = request.form.get("state")
  venue.phone = request.form.get("phone")
  venue.website = request.form.get("website")
  venue.facebook_link = request.form.get("facebook_link")
  venue.seeking_talent = (request.form.get("seeking_talent") == 'y')
  venue.seeking_description = request.form.get("seeking_description")
  venue.image_link = request.form.get("image_link")
  print(venue)
  error = False
  try:
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  if error:
    flash('Venue {} could not be edited!'.format(venue_id))
  else:
    flash('Venue {} was successfully edited'.format(venue_id))
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  artist = Artist()
  error = False
  artist.name = request.form.get('name')
  artist.genres = ','.join(request.form.getlist("genres"))
  artist.city = request.form.get("city")
  artist.state = request.form.get("state")
  artist.phone = request.form.get("phone")
  artist.website = request.form.get("website")
  artist.facebook_link = request.form.get("facebook_link")
  artist.seeking_venue = (request.form.get("seeking_venue")=='y')
  artist.seeking_description = request.form.get("seeking_description")
  artist.image_link = request.form.get("image_link")
  
  try:
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    flash('Artist {} could not be listed'.format(artist.name))
  else:
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.all()
  print(len(shows),"Anzahl Shows:")
  data = []
  for show in shows:
    print('nextShow:{}'.format(show))
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    })

  print(data)

#  data=[{
#    "venue_id": 1,
#    "venue_name": "The Musical Hop",
#    "artist_id": 4,
#    "artist_name": "Guns N Petals",
#    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#    "start_time": "2019-05-21T21:30:00.000Z"
#  }, {
#    "venue_id": 3,
#    "venue_name": "Park Square Live Music & Coffee",
#    "artist_id": 5,
#    "artist_name": "Matt Quevedo",
#    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
#    "start_time": "2019-06-15T23:00:00.000Z"
#  }, {
#    "venue_id": 3,
#    "venue_name": "Park Square Live Music & Coffee",
#    "artist_id": 6,
#    "artist_name": "The Wild Sax Band",
#    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#    "start_time": "2035-04-01T20:00:00.000Z"
#  }, {
#    "venue_id": 3,
#    "venue_name": "Park Square Live Music & Coffee",
#    "artist_id": 6,
#    "artist_name": "The Wild Sax Band",
#    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#    "start_time": "2035-04-08T20:00:00.000Z"
#  }, {
#    "venue_id": 3,
#    "venue_name": "Park Square Live Music & Coffee",
#    "artist_id": 6,
#    "artist_name": "The Wild Sax Band",
#    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#    "start_time": "2035-04-15T20:00:00.000Z"
#  }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  form.artist_id.choices = [(artist.id, artist.name) for artist in Artist.query.all()]
  form.venue_id.choices = [(venue.id, venue.name) for venue in Venue.query.all()]
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error=False
  show = Show(
    artist_id=request.form.get('artist_id'),
    venue_id=request.form.get('venue_id'),
    start_time=request.form.get('start_time')
  )
  print(show)
  try:
    db.session.add(show)
    db.session.commit()
  except:
    db.session.rollback
    error=True
  finally:
    db.session.close()
  if not error:  
  # on successful db insert, flash success
    flash('Show was successfully listed!')
  else:
    flash('Show could not be listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

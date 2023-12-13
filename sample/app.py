from bottle import Bottle, run, template, request, redirect
from os import path
from database import Track, Artist, db
import setup

app = Bottle()

@app.route('/')
def index():
    return template('/workspaces/ADSD_web_app/sample/views/index.html')

@app.route('/display_tracks')
def show_tracks():
    tracks = Track.select()
    return template('/workspaces/ADSD_web_app/sample/views/display_tracks.html', tracks=tracks)

@app.route('/add_track')
def add_new_track():
    return template('/workspaces/ADSD_web_app/sample/views/add_track.html')

@app.route('/process_add_track', method='POST')
def process_add_track():
    title = request.forms.get('title')
    artist = request.forms.get('artist')
    album = request.forms.get('album')
    length = request.forms.get('length')
    artist_name = request.forms.get('artist_name')
    year_released = request.forms.get('year_released')
    setup.add_track(title,artist,album,length,artist_name,year_released)
    return show_tracks()

@app.route('/update_track/<track_title>')
def update_track(track_title):
    try:
        track = Track.get(Track.title == track_title)
        return template('/workspaces/ADSD_web_app/sample/views/update_track.html', track=track)
    except Track.DoesNotExist:
        return "Track is not found"

@app.route('/process_update_track', method='POST')
def process_update_track():
   
    try:
        new_title = request.forms.get('new_title')
        new_artist = request.forms.get('new_artist')
        new_album = request.forms.get('new_album')
        new_length = request.forms.get('new_length')
        setup.update_track(new_title=new_title, new_artist=new_artist, new_album=new_album, new_length=new_length)
        return show_tracks()
    
    except Track.DoesNotExist:
        return "Track not found"
    
@app.route('/delete_track')
def delete_track():
    return redirect('/')

@app.route('/process_delete_track', method='POST')
def process_delete_track():
    track_title = request.forms.get('track_title') 
    
    try:
        setup.delete_track(track_title)
        return show_tracks()
    except Track.DoesNotExist:
        return "Track not found"

@app.route('/display_artists')
def show_artists(): 
    artists= Artist.select()
    return template('/workspaces/ADSD_web_app/sample/views/display_artists.html', artists=artists)

@app.route('/update_artist/<artist_name>')
def update_artist(artist_name):
    try:
        artist=Artist.get(Artist.artist_name==artist_name)
        return template('/workspaces/ADSD_web_app/sample/views/update_artists.html', artist=artist)
    except Artist.DoesNotExist:
        return "Artist not found"

@app.route('/process_update_artist', method='POST')
def process_update_artist():
    #artist_name = request.forms.get('artist_name')
    try:
        artist_name = request.forms.get('artist_name')
        new_artist_name = request.forms.get('new_artist_name')
        new_year_released = request.forms.get('new_year_released')
        setup.update_artist(artist_name=artist_name, new_artist_name=new_artist_name,new_year_released=new_year_released)
        return show_artists()
    except Artist.DoesNotExist:
        return "Artist not found"

@app.route('/search_track')
def search_track():
    search_query = request.query.get('query')
    tracks = setup.search_track(search_query=search_query)
    return template('sample/views/display_tracks.html', tracks=tracks)

if __name__ == '__main__':
    db.connect()
    run(app, host='localhost', port=8000, debug=True)

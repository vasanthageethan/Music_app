from bottle import Bottle, run, template, request, redirect
from os import path
from database import Track, Artist, db
import setup

app = Bottle()

# Define routes

@app.route('/')
def index():
    return template('/workspaces/ADSD_web_app/sample/views/index.html')

@app.route('/display_tracks')
def show_tracks():
    tracks = Track.select()
    track_list = []
    if tracks:
        for track in tracks:
            track_data = {
                'title': track.title,
                'artist': track.artist,
                'album': track.album,
                'length': track.length
            }
            track_list.append(track_data)
    return template('/workspaces/ADSD_web_app/sample/views/display_tracks.html', tracks=track_list)

@app.route('/add_track')
def add_new_track():
    return template('/workspaces/ADSD_web_app/sample/views/add_track.html')

@app.route('/process_add_track', method='POST')
def process_add_track():
    # Retrieve form data
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
    new_title = request.forms.get('new_title')

    try:
       # track = Track.get(Track.title == new_title)
        new_artist = request.forms.get('new_artist')
        new_album = request.forms.get('new_album')
        new_length = request.forms.get('new_length')
        setup.update_track(new_title=new_title, new_artist=new_artist, new_album=new_album, new_length=new_length)
        return show_tracks()
        #return redirect('/display_tracks')
        #print(f"Updated Track {track.track_id}: {track.title} - {track.artist}")
    except Track.DoesNotExist:
        return "Track not found"
    

@app.route('/delete_track')
def delete_track():
    return redirect('/')

@app.route('/process_delete_track', method='POST')
def process_delete_track():
    track_title = request.forms.get('track_title')  # Assuming the form sends the track title to delete
    
    try:
        setup.delete_track(track_title)
        return show_tracks()
    except Track.DoesNotExist:
        return "Track not found"
    except Exception as e:
        return f"An error occurred: {e}"

# Run the app
if __name__ == '__main__':
    db.connect()
    run(app, host='localhost', port=8080, debug=True)

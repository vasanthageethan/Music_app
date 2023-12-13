from database import Track, Artist, db

def display_tracks(id=None):
    if id == None:
        tracks = Track.select()
        print(f"Number of tracks: {tracks.count()}") 
        for track in tracks:
            print(f"Title: {track.title}, Artist: {track.artist}, Album: {track.album}, Length: {track.length}")
        
    else:
        track = Track.get_by_id(id)
        print(f"Title: {track.title}, Artist: {track.artist}, Album: {track.album}, Length: {track.length}")
    db.close()
    
def add_track(title, artist, album, length, artist_name, year_released):
    new_track=Track.create(title=title, artist=artist, album=album, length=length)
    add_artist(new_track,artist_name, year_released)
    db.close()
    

def update_track( new_title, new_artist=None, new_album=None, new_length=None):
    tracks = Track.select().where(Track.title == new_title)
    try:
        for track in tracks:

            if new_artist:
                track.artist = new_artist
            if new_album:
                track.album = new_album
            if new_length:
                track.length = new_length

            track.save()
        display_tracks()
        #print(f"Updated Track {track.title} - {track.artist}")
    except Track.DoesNotExist:
        print("Track not found")
    db.close()
                  
def delete_track(title):
    try:
        track = Track.get(Track.title==title)
        track.delete_instance()
        print(f"Deleted Track {track.title} - {track.artist}")
        display_tracks()
    except Track.DoesNotExist:
        print("Track not found")
    db.close()

def search_track(search_query):
    tracks = Track.select().where((Track.title.contains(search_query)) | (Track.album.contains(search_query)))

    if tracks:
        print(f"Found tracks matching '{search_query}':")
        for track in tracks:
            print(f"Title: {track.title}, Artist: {track.artist}, Album: {track.album}, Length: {track.length}")
    else:
        print(f"No tracks found matching '{search_query}'")
    db.close()

def display_artist(id = None):
    if id == None:
        artists = Artist.select()
        for artist in artists:
            print(f"Artist: {artist.artist_name}, Track_id: {artist.track_id}, Year Released: {artist.year_released}")
    else:
        artist = Artist.select(id)
        print(f"Artist: {artist.artist_name}, Year Released: {artist.year_released}")
    print(f"Count:{artists.count()}")
    db.close()

def add_artist(new_track, artist_name,year_released):
    if Artist.select().where(Artist.artist_name == artist_name).exists()==False:
        Artist.get_or_create(artist_name=artist_name,track_id= new_track.id, year_released= year_released) 
    db.close()

def delete_artist(artist_name):
    try:
        artist = Artist.get(Artist.artist_name == artist_name)
        artist.delete_instance()
        print(f"Deleted artist: {artist_name}")
    except Artist.DoesNotExist:
        print(f"Artist '{artist_name}' not found")
    display_artist()
    db.close()

def update_artist(artist_name, new_artist_name, year_released= None):
    try:
        artist = Artist.get(Artist.artist_name == artist_name)
        if artist_name:
            artist.artist_name = new_artist_name
        if year_released:
            artist.year_released = year_released
        artist.save()
        print(f"Artist: {artist.artist_name}, Year Released: {artist.year_released}")

    except Artist.DoesNotExist:
        print(f" Artist does not exist ")
    db.close()

if __name__ == "__main__":

    db.connect()
    add_track("enthiran", "arrw", "enthiran", 180, "arrahman", 2019)
    add_track("vilayadu", "yuvan", "mankatha", 190, "yuvan", 2015)
    add_track("kannathil muthamital", "raja", "mankatha", 190, "raja", 2010)
    add_track("kannathil muthamital", "raja", "mankatha", 190, "raja", 2010)
    add_track("vilayadu", "yuvan", "mankatha", 190, "yuvan", 2015)
    add_track("valayosai", "raja", "movie", 190, "raja", 1999)
    #update_track("vilayadu","yuvan","mohan",190)
    #delete_track("enthiran")
    #update_artist("yuvan")
    display_artist()
    #display_tracks()
   # delete_track(1)
   # display_tracks(3)
   # test_update_track()
   # search_track("enthiran")
   

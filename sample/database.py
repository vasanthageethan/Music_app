from peewee import *

# Define the database (SQLite in this case)
db = SqliteDatabase('music_library.db')

# Define the model for the Track table
class Track(Model):
    title = CharField()
    artist = CharField()#(Artist, field=Artist.artist_id, backref='tracks')# artist = ForeignKeyField(Artist, backref='tracks')
    album = CharField()
    length = IntegerField()

    class Meta:
        database = db  # Connect the model to the database
        
class Artist(Model):
    artist_name = CharField()
    artist_id = AutoField(unique=True)
    track_id = ForeignKeyField(Track, backref='artists')
    year_released = IntegerField()

    class Meta:
        database = db 




with db:
    db.drop_tables([Artist, Track])  # Drop existing tables
    db.create_tables([Artist, Track]) 
    sample_tracks = [
    {"title": "Track 1", "artist": "Artist 1", "album": "Album 1", "length": 180, "year_released":1999 },
    {"title": "Track 2", "artist": "Artist 2", "album": "Album 2", "length": 200, "year_released":2010},
    {"title": "Track 3", "artist": "Artist 3", "album": "Album 3", "length": 220, "year_released":2005},
]

# Populating the Track table with sample data
for track_data in sample_tracks:
    # Create or get the Artist instance
    #artist, _ = Artist.get_or_create(artist_name=track_data['artist'], year_released=2023)

    # Create a Track instance and link it to the Artist
    Track.create(
        title=track_data['title'],
        artist=track_data['artist'],
        album=track_data['album'],
        length=track_data['length']
    )
    
    db.close()
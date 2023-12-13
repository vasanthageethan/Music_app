from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Create a connection to SQLite database
conn = sqlite3.connect('music_albums.db', check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS albums (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    artist TEXT,
                    year_released INTEGER,
                    genre TEXT
                )''')
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

# GET all albums
@app.route('/api/albums', methods=['GET'])
def get_albums():
    cursor.execute("SELECT * FROM albums")
    albums = cursor.fetchall()
    return jsonify(albums)

# POST a new album
@app.route('/api/albums', methods=['POST'])
def add_album():
    data = request.get_json()
    title = data['title']
    artist = data['artist']
    year_released = data['year_released']
    genre = data['genre']
    cursor.execute("INSERT INTO albums (title, artist, year_released, genre) VALUES (?, ?, ?, ?)",
                   (title, artist, year_released, genre))
    conn.commit()
    return jsonify({"message": "Album added successfully!"})

# PUT (Update) an album
@app.route('/api/albums/<int:id>', methods=['PUT'])
def update_album(id):
    data = request.get_json()
    title = data['title']
    artist = data['artist']
    year_released = data['year_released']
    genre = data['genre']
    cursor.execute("UPDATE albums SET title=?, artist=?, year_released=?, genre=? WHERE id=?",
                   (title, artist, year_released, genre, id))
    conn.commit()
    return jsonify({"message": "Album updated successfully!"})

# DELETE an album
@app.route('/api/albums/<int:id>', methods=['DELETE'])
def delete_album(id):
    cursor.execute("DELETE FROM albums WHERE id=?", (id,))
    conn.commit()
    return jsonify({"message": "Album deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)

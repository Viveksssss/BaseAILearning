import os
import sqlite3

db_path = "resources/Chinook.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS Playlist (    PlaylistId INTEGER PRIMARY KEY AUTOINCREMENT,    Name TEXT);
    """)
playlists_data = [    (1, "Music"),    (2, "Movies"),    (3, "TV Shows"),    (4, "Audiobooks"),    (5, "90’s Music"),    (6, "Audiobooks"),    (7, "Movies"),    (8, "Music"),    (9, "Music Videos"),    (10, "TV Shows"),    (11, "Brazilian Music"),    (12, "Classical"),    (13, "Classical 101 - Deep Cuts"),    (14, "Classical 101 - Next Steps"),    (15, "Classical 101 - The Basics"),    (16, "Grunge"),    (17, "Heavy Metal Classic"),    (18, "On-The-Go 1"),
]

cursor.executemany("INSERT OR IGNORE INTO Playlist (PlaylistId, Name) VALUES (?, ?)",playlists_data
)


conn.commit()
conn.close()
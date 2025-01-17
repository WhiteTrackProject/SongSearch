import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="songsearch.db"):
        self.connection = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        """Crea las tablas necesarias en la base de datos."""
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS songs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    artist TEXT,
                    path TEXT UNIQUE NOT NULL,
                    duration INTEGER,
                    format TEXT,
                    size INTEGER,
                    modified_date TEXT
                )
            """)

    def add_song(self, name, artist, path, duration, file_format, size, modified_date):
        """Añade una canción a la base de datos."""
        with self.connection:
            self.connection.execute("""
                INSERT OR IGNORE INTO songs (name, artist, path, duration, format, size, modified_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, artist, path, duration, file_format, size, modified_date))

    def search_song(self, query):
        """Busca canciones en la base de datos por nombre o artista."""
        with self.connection:
            return self.connection.execute("""
                SELECT * FROM songs
                WHERE name LIKE ? OR artist LIKE ?
            """, (f"%{query}%", f"%{query}%")).fetchall()

    def list_all_songs(self):
        """Lista todas las canciones en la base de datos."""
        with self.connection:
            return self.connection.execute("SELECT * FROM songs").fetchall()

import sqlite3

class Concert:
    def __init__(self, id, band_id, venue_id, date):
        self.id = id
        self.band_id = band_id
        self.venue_id = venue_id
        self.date = date

    @staticmethod
    def band(concert_id):
        conn = sqlite3.connect('concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT bands.name, bands.hometown
            FROM concerts
            JOIN bands ON concerts.band_id = bands.id
            WHERE concerts.id = ?
        ''', (concert_id,))
        band = cursor.fetchone()
        conn.close()
        return band

    @staticmethod
    def venue(concert_id):
        conn = sqlite3.connect('concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT venues.title, venues.city
            FROM concerts
            JOIN venues ON concerts.venue_id = venues.id
            WHERE concerts.id = ?
        ''', (concert_id,))
        venue = cursor.fetchone()
        conn.close()
        return venue

class Band:
    def __init__(self, id, name, hometown):
        self.id = id
        self.name = name
        self.hometown = hometown

    def concerts(self):
        conn = sqlite3.connect('concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM concerts WHERE band_id = ?
        ''', (self.id,))
        concerts = cursor.fetchall()
        conn.close()
        return concerts

    def venues(self):
        conn = sqlite3.connect('concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT venues.title, venues.city
            FROM concerts
            JOIN venues ON concerts.venue_id = venues.id
            WHERE concerts.band_id = ?
        ''', (self.id,))
        venues = cursor.fetchall()
        conn.close()
        return venues

class Venue:
    def __init__(self, id, title, city):
        self.id = id
        self.title = title
        self.city = city

    def concerts(self):
        conn = sqlite3.connect('concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM concerts WHERE venue_id = ?
        ''', (self.id,))
        concerts = cursor.fetchall()
        conn.close()
        return concerts

    def bands(self):
        conn = sqlite3.connect('concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT bands.name, bands.hometown
            FROM concerts
            JOIN bands ON concerts.band_id = bands.id
            WHERE concerts.venue_id = ?
        ''', (self.id,))
        bands = cursor.fetchall()
        conn.close()
        return bands



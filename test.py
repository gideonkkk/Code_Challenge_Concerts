import unittest
import sqlite3
from concerts import Concert
from bands import Band
from venues import Venue

class TestConcerts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test database and tables"""
        cls.conn = sqlite3.connect(':memory:')  # Use an in-memory database for testing
        cls.cursor = cls.conn.cursor()

        # Create tables
        cls.cursor.execute('''
            CREATE TABLE bands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                hometown TEXT NOT NULL
            )
        ''')
        
        cls.cursor.execute('''
            CREATE TABLE venues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                city TEXT NOT NULL
            )
        ''')

        cls.cursor.execute('''
            CREATE TABLE concerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                band_id INTEGER,
                venue_id INTEGER,
                date TEXT,
                FOREIGN KEY (band_id) REFERENCES bands(id),
                FOREIGN KEY (venue_id) REFERENCES venues(id)
            )
        ''')

        # Insert test data
        cls.cursor.execute("INSERT INTO bands (name, hometown) VALUES ('Band A', 'City X')")
        cls.cursor.execute("INSERT INTO bands (name, hometown) VALUES ('Band B', 'City Y')")
        cls.cursor.execute("INSERT INTO venues (title, city) VALUES ('Venue 1', 'City X')")
        cls.cursor.execute("INSERT INTO venues (title, city) VALUES ('Venue 2', 'City Y')")
        cls.cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (1, 1, '2024-01-01')")
        cls.cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (2, 2, '2024-01-02')")

        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        """Close the database connection"""
        cls.conn.close()

    def test_concert_band(self):
        """Test Concert.band() method"""
        concert = Concert(self.conn, 1)
        band = concert.band()
        self.assertEqual(band['name'], 'Band A')
        self.assertEqual(band['hometown'], 'City X')

    def test_concert_venue(self):
        """Test Concert.venue() method"""
        concert = Concert(self.conn, 1)
        venue = concert.venue()
        self.assertEqual(venue['title'], 'Venue 1')
        self.assertEqual(venue['city'], 'City X')

    def test_venue_concerts(self):
        """Test Venue.concerts() method"""
        venue = Venue(self.conn, 1)
        concerts = venue.concerts()
        self.assertEqual(len(concerts), 1)
        self.assertEqual(concerts[0]['date'], '2024-01-01')

    def test_venue_bands(self):
        """Test Venue.bands() method"""
        venue = Venue(self.conn, 1)
        bands = venue.bands()
        self.assertEqual(len(bands), 1)
        self.assertEqual(bands[0]['name'], 'Band A')

    def test_band_concerts(self):
        """Test Band.concerts() method"""
        band = Band(self.conn, 1)
        concerts = band.concerts()
        self.assertEqual(len(concerts), 1)
        self.assertEqual(concerts[0]['date'], '2024-01-01')

    def test_band_venues(self):
        """Test Band.venues() method"""
        band = Band(self.conn, 1)
        venues = band.venues()
        self.assertEqual(len(venues), 1)
        self.assertEqual(venues[0]['title'], 'Venue 1')

    def test_concert_hometown_show(self):
        """Test Concert.hometown_show() method"""
        concert = Concert(self.conn, 1)
        self.assertTrue(concert.hometown_show())
        concert = Concert(self.conn, 2)
        self.assertFalse(concert.hometown_show())

    def test_concert_introduction(self):
        """Test Concert.introduction() method"""
        concert = Concert(self.conn, 1)
        intro = concert.introduction()
        self.assertEqual(intro, "Hello City X!!!!! We are Band A and we're from City X")

    def test_band_play_in_venue(self):
        """Test Band.play_in_venue() method"""
        band = Band(self.conn, 1)
        band.play_in_venue('Venue 2', '2024-01-03')
        self.cursor.execute("SELECT * FROM concerts WHERE band_id = 1 AND venue_id = 2 AND date = '2024-01-03'")
        concert = self.cursor.fetchone()
        self.assertIsNotNone(concert)

    def test_band_all_introductions(self):
        """Test Band.all_introductions() method"""
        band = Band(self.conn, 1)
        intros = band.all_introductions()
        self.assertEqual(len(intros), 1)
        self.assertEqual(intros[0], "Hello City X!!!!! We are Band A and we're from City X")

    def test_band_most_performances(self):
        """Test Band.most_performances() method"""
        band = Band(self.conn, 1)
        most_performances_band = band.most_performances()
        self.assertEqual(most_performances_band['name'], 'Band A')

    def test_venue_concert_on(self):
        """Test Venue.concert_on() method"""
        venue = Venue(self.conn, 1)
        concert = venue.concert_on('2024-01-01')
        self.assertIsNotNone(concert)
        self.assertEqual(concert['date'], '2024-01-01')

    def test_venue_most_frequent_band(self):
        """Test Venue.most_frequent_band() method"""
        venue = Venue(self.conn, 1)
        most_frequent_band = venue.most_frequent_band()
        self.assertEqual(most_frequent_band['name'], 'Band A')

if __name__ == '__main__':
    unittest.main()

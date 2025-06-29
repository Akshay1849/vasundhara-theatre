import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Delete old bookings table if it exists
c.execute("DROP TABLE IF EXISTS bookings")

# Create a new bookings table with updated columns (including 'seats')
c.execute('''
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER,
    movie_title TEXT,
    name TEXT,
    phone TEXT,
    showtime TEXT,
    category TEXT,
    count INTEGER,
    total_price INTEGER,
    seats TEXT,
    booking_time TEXT
);
''')

conn.commit()
conn.close()

print("✅ Fixed: 'bookings' table recreated with all required columns including 'seats'")

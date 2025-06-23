import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Delete old table if exists
c.execute("DROP TABLE IF EXISTS bookings")

# Create new table with updated columns
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
    booking_time TEXT
);
''')

conn.commit()
conn.close()
print("✅ Fixed: Bookings table recreated with correct columns")

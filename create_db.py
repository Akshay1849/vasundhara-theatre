import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create Movies Table
c.execute('''
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    poster TEXT,
    language TEXT,
    cast TEXT,
    duration TEXT,
    status TEXT  -- running / upcoming
)
''')

# Add a sample movie (you can change or add more later)
c.execute("INSERT INTO movies (title, poster, language, cast, duration, status) VALUES (?, ?, ?, ?, ?, ?)",
          ("Pushpa 2", "pushpa2.jpg", "Telugu", "Allu Arjun", "2hr 45min", "running"))

conn.commit()
conn.close()

print("✅ Database created successfully!")

import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Add 'seats' column if not exists
try:
    cursor.execute("ALTER TABLE bookings ADD COLUMN seats TEXT;")
    print("✅ 'seats' column added to 'bookings' table.")
except sqlite3.OperationalError as e:
    print("⚠️ Error:", e)

conn.commit()
conn.close()

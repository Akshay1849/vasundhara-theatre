from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

# Flask App Initialization
app = Flask(__name__)
app.secret_key = "vasundhara_secret_2025"

# -----------------------------
# DATABASE CONNECTION FUNCTION
# -----------------------------
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# -----------------
# HOME PAGE ROUTE
# -----------------
@app.route('/')
def home():
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movies ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('home.html', movies=movies)

# -----------------
# BOOKING PAGE
# -----------------
@app.route('/book/<int:movie_id>')
def book(movie_id):
    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM movies WHERE id=?', (movie_id,)).fetchone()
    conn.close()
    if movie:
        return render_template('book.html', movie=movie)
    return "Movie not found"

# --------------------------
# CONFIRM BOOKING
# --------------------------
@app.route('/confirm_booking/<int:movie_id>', methods=['POST'])
def confirm_booking(movie_id):
    name = request.form['name']
    phone = request.form['phone']
    showtime = request.form['showtime']
    count = int(request.form['count'])
    seats = request.form['seats']
    seat_list = seats.split(',')

    # Calculate total price based on seat prefix (U- or L-)
    total_price = 0
    upper_count = 0
    lower_count = 0
    for seat in seat_list:
        if seat.startswith('U-'):
            total_price += 100
            upper_count += 1
        elif seat.startswith('L-'):
            total_price += 80
            lower_count += 1

    booking_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM movies WHERE id=?', (movie_id,)).fetchone()

    conn.execute('''
        INSERT INTO bookings (movie_id, movie_title, name, phone, showtime, category, count, total_price, seats, booking_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        movie['id'],
        movie['title'],
        name,
        phone,
        showtime,
        'Mixed',  # Now it's mixed, so we use a label like "Mixed"
        count,
        total_price,
        seats,
        booking_time
    ))

    conn.commit()
    conn.close()

    return render_template('confirmation.html',
                           movie=movie,
                           name=name,
                           phone=phone,
                           showtime=showtime,
                           category='Mixed',
                           count=count,
                           upper_count=upper_count,
                           lower_count=lower_count,
                           total_price=total_price,
                           booking_time=booking_time,
                           seats=seats)

# --------------------
# LOGIN
# --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == '1234':
            session['admin'] = True
            return redirect(url_for('admin'))
        return "Invalid credentials"
    return render_template('login.html')

# --------------------
# LOGOUT
# --------------------
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

# --------------------------
# ADMIN PANEL
# --------------------------
@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movies ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('admin.html', movies=movies)

# ------------------------------
# ADMIN: ADD MOVIE
# ------------------------------
@app.route('/admin/add_movie', methods=['GET', 'POST'])
def add_movie():
    if not session.get('admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        poster = request.form['poster']
        language = request.form['language']
        cast = request.form['cast']
        duration = request.form['duration']
        status = request.form['status']

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO movies (title, poster, language, cast, duration, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, poster, language, cast, duration, status))
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))

    return render_template('add_movie.html')

# ------------------------------
# ADMIN: EDIT MOVIE
# ------------------------------
@app.route('/admin/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    if not session.get('admin'):
        return redirect(url_for('login'))

    conn = get_db_connection()

    if request.method == 'POST':
        title = request.form['title']
        poster = request.form['poster']
        language = request.form['language']
        cast = request.form['cast']
        duration = request.form['duration']
        status = request.form['status']

        conn.execute('''
            UPDATE movies SET title=?, poster=?, language=?, cast=?, duration=?, status=? WHERE id=?
        ''', (title, poster, language, cast, duration, status, movie_id))
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))

    movie = conn.execute('SELECT * FROM movies WHERE id=?', (movie_id,)).fetchone()
    conn.close()
    return render_template('edit_movie.html', movie=movie)

# ------------------------------
# ADMIN: DELETE MOVIE
# ------------------------------
@app.route('/admin/delete_movie/<int:movie_id>')
def delete_movie(movie_id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM movies WHERE id=?', (movie_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

# --------------------------
# RUN FLASK APP
# --------------------------
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime  # ✅ to track booking time
import os

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
    category = request.form['category']
    count = int(request.form['count'])

    price_per_ticket = 100 if category == 'upper' else 80
    total_price = price_per_ticket * count
    booking_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM movies WHERE id=?', (movie_id,)).fetchone()

    conn.execute('''
        INSERT INTO bookings (movie_id, movie_title, name, phone, showtime, category, count, total_price, booking_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (movie['id'], movie['title'], name, phone, showtime, category, count, total_price, booking_time))
    conn.commit()
    conn.close()

    return render_template('confirmation.html',
                           movie=movie,
                           name=name,
                           phone=phone,
                           showtime=showtime,
                           category=category,
                           count=count,
                           total_price=total_price,
                           booking_time=booking_time)

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

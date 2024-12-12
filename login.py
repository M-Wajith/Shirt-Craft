from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import sqlite3

login_bp = Blueprint('login', __name__, template_folder='templates')

def get_db_connection():
    conn = sqlite3.connect('D:/Wajith/Shirt Craft/shirtcraft.db')
    conn.row_factory = sqlite3.Row
    return conn

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and Password are required.')
            return redirect(url_for('login.login'))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Admin WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials, please try again')

    return render_template('login.html')

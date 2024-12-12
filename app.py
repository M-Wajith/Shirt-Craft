from flask import Flask, render_template, redirect, url_for, flash, request, session, abort, send_from_directory, send_file,  jsonify
from utils import get_db_connection, get_fabrics_data, get_fabric_image, get_fabric_details, filter_fabrics
from io import BytesIO
from flask import Response
import os
from login import login_bp
from admin import admin_bp
from addfabric import addfabric_bp
from editfabric import edit_fabric_bp
from deletefabric import delete_fabric_bp
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.register_blueprint(login_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(addfabric_bp)
app.register_blueprint(edit_fabric_bp)
app.register_blueprint(delete_fabric_bp)


@app.route('/')
def index():
    fabrics, colors, materials, prices, patterns, categories = get_fabrics_data()
    return render_template('index.html', fabrics=fabrics, colors=colors, materials=materials, prices=prices, patterns=patterns, categories = categories)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    response = redirect(url_for('login.login'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

static_js_dir = r"D:\Wajith\Shirt Craft\static\js"
static_model_dir = r"D:\Wajith\Shirt Craft\static\models"

@app.route('/static/js/<filename>')
def serve_js_files(filename):
    # Sanitize and ensure the file exists in the directory
    if os.path.exists(os.path.join(static_js_dir, filename)):
        return send_from_directory(static_js_dir, filename)
    else:
        abort(404)

@app.route('/static/models/<filename>')
def serve_model_files(filename):
    return send_from_directory(static_model_dir, filename)





@app.route('/filter_fabrics', methods=['POST'])
def filter_fabrics_route():
    filters = {
        'color': request.form.get('color'),
        'material': request.form.get('material'),
        'price': request.form.get('price'),
        'pattern': request.form.get('pattern'),
        'category': request.form.get('category')
    }
    
    try:
        fabrics, colors, materials, prices, patterns, categories = filter_fabrics(filters)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for('index'))

    return render_template('index.html', fabrics=fabrics, colors=colors, materials=materials, prices=prices, patterns=patterns, categories=categories)


@app.route('/fabric_image/<fabric_id>')
def fabric_image(fabric_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT fabric_image FROM Fabrics WHERE fabric_id = ?", (fabric_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        print(f"Fabric ID {fabric_id} image fetched")
        return send_file(BytesIO(row[0]), mimetype='image/jpeg')
    else:
        print(f"Fabric ID {fabric_id} image not found")
        abort(404)


@app.route('/fabric_details/<fabric_id>')
def fabric_details(fabric_id):
    return get_fabric_details(fabric_id)

@app.route('/get-fabric/<fabric_id>', methods=['GET'])
def get_fabric(fabric_id):
    fabric_image = get_fabric_image(fabric_id)
    if fabric_image:
        return send_file(BytesIO(fabric_image), mimetype='image/jpeg')
    else:
        return jsonify({'error': 'Fabric not found'}), 404
    
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            # If not logged in, redirect to login page
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated_function
    

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Admin dashboard logic here
    return "Welcome to Admin Dashboard"


if __name__ == '__main__':
    app.run(debug=True)

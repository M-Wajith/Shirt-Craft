from flask import Blueprint, render_template, redirect, url_for, request, session, make_response, flash
from utils import get_db_connection, get_fabrics_data, get_fabric_image, get_fabric_details, filter_fabrics
from addfabric import addfabric_bp
from editfabric import edit_fabric_bp



admin_bp = Blueprint('admin', __name__, template_folder='templates')

admin_bp.register_blueprint(addfabric_bp)
admin_bp.register_blueprint(edit_fabric_bp, url_prefix='/admin')

@admin_bp.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login.login'))

    fabrics, colors, materials, prices, patterns, categories = get_fabrics_data()
    print("Colors:", colors)
    print("Materials:", materials)
    print("Prices:", prices)
    print("Patterns:", patterns)
    print("Categories:", categories)
    response = make_response(render_template('admin.html', fabrics=fabrics, colors=colors, materials=materials, prices=prices, patterns=patterns, categories = categories))
    # Prevent caching
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@admin_bp.route('/fabric_details/<fabric_id>')
def fabric_details(fabric_id):
    if not session.get('logged_in'):
        return redirect(url_for('login.login'))

    fabric = get_fabric_details(fabric_id)
    return render_template('fabric_details.html', fabric=fabric)

@admin_bp.route('/fabric_image/<fabric_id>')
def fabric_image(fabric_id):
    if not session.get('logged_in'):
        return redirect(url_for('login.login'))

    return get_fabric_image(fabric_id)

@admin_bp.route('/dashboard')
def add_dashboard():
    # Admin dashboard logic
    return render_template('admin.html')


@admin_bp.route('/admin_filter_fabrics', methods=['POST'])
def admin_filter_fabrics():
    filters = {
        'color': request.form.get('color'),
        'material': request.form.get('material'),
        'price': request.form.get('price'),
        'pattern': request.form.get('pattern'),
        'category':request.form.get('category')
    }
    
    query = 'SELECT fabric_id, fabric_name FROM Fabrics WHERE 1=1'
    params = []

    for key, value in filters.items():
        if value:
            if key == 'price':
                try:
                    price_min, price_max = value.split('-')
                    query += " AND fabric_price BETWEEN ? AND ?"
                    params.extend([price_min, price_max])
                except ValueError:
                    flash('Invalid price range format.')
                    return redirect(url_for('index'))
            else:
                query += f" AND fabric_{key} = ?"
                params.append(value)

    conn = get_db_connection()
    c = conn.cursor()
    c.execute(query, tuple(params))
    fabrics = c.fetchall()
    
    c.execute('SELECT DISTINCT fabric_color FROM Fabrics WHERE fabric_color IS NOT NULL')
    colors = c.fetchall()

    c.execute('SELECT DISTINCT fabric_material FROM Fabrics WHERE fabric_material IS NOT NULL')
    materials = c.fetchall()
    
    c.execute('SELECT DISTINCT fabric_price FROM Fabrics WHERE fabric_price IS NOT NULL')
    prices = c.fetchall()
    
    c.execute('SELECT DISTINCT fabric_pattern FROM Fabrics WHERE fabric_pattern IS NOT NULL')
    patterns = c.fetchall()

    c.execute('SELECT DISTINCT fabric_category FROM Fabrics WHERE fabric_pattern IS NOT NULL')
    categories = c.fetchall()

    conn.close()
    
    return render_template('admin.html', fabrics=fabrics, colors=colors, materials=materials, prices=prices, patterns=patterns, categories=categories)

    
    try:
        fabrics, colors, materials, prices, patterns = filter_fabrics(filters)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for('admin.dashboard'))

    return render_template('admin.html', fabrics=fabrics, colors=colors, materials=materials, prices=prices, patterns=patterns, categories= categories)

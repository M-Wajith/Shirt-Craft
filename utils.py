import sqlite3
import io
from flask import abort, send_file

def get_db_connection():
    conn = sqlite3.connect('D:/Wajith/Shirt Craft/shirtcraft.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_fabrics_data():
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('SELECT fabric_id, fabric_name, fabric_color, fabric_material, fabric_price, fabric_pattern, fabric_category FROM Fabrics')
        fabrics = c.fetchall()

        c.execute('SELECT DISTINCT fabric_color FROM Fabrics WHERE fabric_color IS NOT NULL')
        colors = c.fetchall()

        c.execute('SELECT DISTINCT fabric_material FROM Fabrics WHERE fabric_material IS NOT NULL')
        materials = c.fetchall()

        c.execute('SELECT DISTINCT fabric_price FROM Fabrics WHERE fabric_price IS NOT NULL')
        prices = c.fetchall()

        c.execute('SELECT DISTINCT fabric_pattern FROM Fabrics WHERE fabric_pattern IS NOT NULL')
        patterns = c.fetchall()

        c.execute('SELECT DISTINCT fabric_category FROM Fabrics WHERE fabric_category IS NOT NULL')
        categories = c.fetchall()

        conn.close()
        return fabrics, colors, materials, prices, patterns, categories
    except Exception as e:
        conn.close()
        abort(500, description=str(e))

def get_fabric_image(fabric_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT fabric_image FROM Fabrics WHERE fabric_id = ?', (fabric_id,))
    image_data = c.fetchone()
    conn.close()
    
    if image_data and image_data['fabric_image']:
        return send_file(
            io.BytesIO(image_data['fabric_image']),
            mimetype='image/jpeg',
            as_attachment=False,
            download_name=f'{fabric_id}.jpg'
        )
    else:
        abort(404, description="Image not found")

def get_fabric_details(fabric_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM Fabrics WHERE fabric_id = ?', (fabric_id,))
    fabric = c.fetchone()
    conn.close()

    if fabric:
        return {
            'image_url': '/fabric_image/' + fabric['fabric_id'],
            'name': fabric['fabric_name'],
            'material': fabric['fabric_material'],
            'color': fabric['fabric_color'],
            'price': fabric['fabric_price'],
            'pattern': fabric['fabric_pattern'],
            'category':fabric['fabric_category']
        }
    else:
        abort(404)

def filter_fabrics(filters):
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
                    raise ValueError('Invalid price range format.')
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

    c.execute('SELECT DISTINCT fabric_category FROM Fabrics WHERE fabric_category IS NOT NULL')
    categories = c.fetchall()

    conn.close()
    
    return fabrics, colors, materials, prices, patterns, categories





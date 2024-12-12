from flask import Blueprint, request, jsonify, render_template
import sqlite3

edit_fabric_bp = Blueprint('edit_fabric_bp', __name__)

def get_db_connection():
    conn = sqlite3.connect('D:/Wajith/Shirt Craft/shirtcraft.db')
    conn.row_factory = sqlite3.Row
    return conn

# Update fabric details in the database
def update_fabric(fabric_id, fabric_name, fabric_color, fabric_material, fabric_price, fabric_pattern, fabric_category, fabric_image_data=None):
    conn = get_db_connection()
    try:
        if fabric_image_data:
            conn.execute('''
                UPDATE Fabrics
                SET fabric_name = ?, fabric_color = ?, fabric_material = ?, fabric_price = ?, 
                    fabric_pattern = ?, fabric_category = ?, fabric_image = ?
                WHERE fabric_id = ?''',
                (fabric_name, fabric_color, fabric_material, fabric_price, fabric_pattern, fabric_category, fabric_image_data, fabric_id))
        else:
            conn.execute('''
                UPDATE Fabrics
                SET fabric_name = ?, fabric_color = ?, fabric_material = ?, fabric_price = ?, 
                    fabric_pattern = ?, fabric_category = ?
                WHERE fabric_id = ?''',
                (fabric_name, fabric_color, fabric_material, fabric_price, fabric_pattern, fabric_category, fabric_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating fabric: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

@edit_fabric_bp.route('/edit_fabric/<fabric_id>', methods=['POST'])
def edit_fabric(fabric_id):
    # Get form data
    fabric_name = request.form.get('name')
    fabric_color = request.form.get('color')
    fabric_material = request.form.get('material')
    fabric_price = request.form.get('price')
    fabric_pattern = request.form.get('pattern')
    fabric_category = request.form.get('category')

    fabric_image = request.files.get('image')
    if fabric_image:
        fabric_image_data = fabric_image.read()
    else:
        fabric_image_data = None

    # Update fabric in the database
    success = update_fabric(fabric_id, fabric_name, fabric_color, fabric_material, fabric_price, fabric_pattern, fabric_category, fabric_image_data)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False}), 500

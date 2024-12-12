from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
from utils import get_db_connection


addfabric_bp = Blueprint('addfabric', __name__, template_folder='templates')

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@addfabric_bp.route('/add_fabric', methods=['POST'])
def add_fabric():
    try:
        # Log the request data
        print(request.form)
        print(request.files)
        # Get fabric details from the form
        fabric_name = request.form.get('fabricName')
        fabric_color = request.form.get('fabricColor')
        fabric_price = request.form.get('fabricPrice')
        fabric_material = request.form.get('fabricMaterial')  # Default to 'Cotton' if not provided
        fabric_pattern = request.form.get('fabricPattern')
        fabric_category = request.form.get('fabricCategory')
        fabric_image = request.files.get('fabricImage')

        # Validate required fields
        if not fabric_name or not fabric_color or not fabric_price or not fabric_category:
            return jsonify({'success': False, 'message': 'Fabric name, color, price, and category are required.'}), 400

        # Handle file upload
        fabric_image_data = None
        if fabric_image and allowed_file(fabric_image.filename):
            fabric_image_data = fabric_image.read()  # Read the file as binary
        elif fabric_image:
            return jsonify({'success': False, 'message': 'Invalid image format. Allowed formats: png, jpg, jpeg, gif.'}), 400

        # Get the last fabric_id from the database
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT fabric_id FROM Fabrics ORDER BY fabric_id DESC LIMIT 1')
        last_fabric = c.fetchone()

        # Generate the new fabric_id
        if last_fabric:
            last_fabric_id = last_fabric[0]
            # Extract the numeric part of the fabric ID (e.g., 'F004' -> 4)
            last_fabric_num = int(last_fabric_id[1:])
            new_fabric_id = f'F{last_fabric_num + 1:03}'  # Increment and format (e.g., 'F004' -> 'F005')
        else:
            # If no records, start from 'F001'
            new_fabric_id = 'F001'

        # Insert fabric details into the database
        query = '''
            INSERT INTO Fabrics (fabric_id, fabric_name, fabric_color, fabric_price, fabric_material, fabric_pattern, fabric_category, fabric_image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        c.execute(query, (new_fabric_id, fabric_name, fabric_color, fabric_price, fabric_material, fabric_pattern, fabric_category, fabric_image_data))
        conn.commit()
        conn.close()

        print(request.form)  # Add this line in your backend code to inspect received form data


        return jsonify({'success': True, 'message': 'Fabric added successfully!'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'An internal error occurred.'}), 500
    
    


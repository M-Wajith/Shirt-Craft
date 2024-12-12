from flask import Blueprint, jsonify
import sqlite3

delete_fabric_bp = Blueprint('delete_fabric_bp', __name__)

def get_db_connection():
    conn = sqlite3.connect('D:/Wajith/Shirt Craft/shirtcraft.db')
    conn.row_factory = sqlite3.Row
    return conn

@delete_fabric_bp.route('/delete_fabric/<fabric_id>', methods=['POST'])
def delete_fabric(fabric_id):
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM Fabrics WHERE fabric_id = ?', (fabric_id,))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error deleting fabric: {e}")
        return jsonify({'success': False}), 500
    finally:
        conn.close()

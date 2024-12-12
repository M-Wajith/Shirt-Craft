import sqlite3

def insert_fabric_data(fabric_id, fabric_name, fabric_color, fabric_pattern, fabric_price, file_path, fabric_category_id, fabric_category, fabric_material='Cotton'):
    # Connect to the database
    conn = sqlite3.connect(r'D:\Wajith\Shirt Craft\shirtcraft.db')
    c = conn.cursor()
    
    # Read image file as binary data
    with open(file_path, 'rb') as file:
        image_data = file.read()
    
    # Insert data into the Fabric table
    c.execute('''
        INSERT INTO Fabrics (fabric_id, fabric_name, fabric_color, fabric_pattern, fabric_price, fabric_image, fabric_category_id, fabric_material, fabric_category) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (fabric_id, fabric_name, fabric_color, fabric_pattern, fabric_price, image_data, fabric_category_id, fabric_material, fabric_category))
    
    # Commit and close the connection
    conn.commit()
    conn.close()

# Example usage
insert_fabric_data(
    fabric_id='F004',
    fabric_name='Blue third',
    fabric_color='Blue',
    fabric_pattern='plain',
    fabric_price=5500,
    file_path=r'D:\Wajith\Shirt Craft\fabrics\casual.jpg', # local path of image
    fabric_category_id=1,
    fabric_category='casual',
    fabric_material='Cotton'  # You can change this if needed
)

print("Fabric Added")

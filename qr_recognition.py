import cv2
import numpy as np
from pyzbar.pyzbar import decode

def read_qr_code(image_path):
    # Read the image
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Use pyzbar to decode QR codes
    decoded_objects = decode(gray)
    
    # Loop through detected QR codes
    qr_code_data = []
    for obj in decoded_objects:
        # Extract data
        data = obj.data.decode('cp866')
        type = obj.type
        
        # If it's a QR code, print data
        if type == 'QRCODE':
            qr_code_data.append(data)
    
    # Return the text
    return ''.join(qr_code_data)

print(read_qr_code("images/unnamed.png"))
import cv2
import numpy as np
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)

qr_code_data = []
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use pyzbar to decode QR codes
    decoded_objects = decode(gray)

    # Loop through detected QR codes
    for obj in decoded_objects:
        # Extract data
        data = obj.data.decode('utf-8')
        type = obj.type

        # If it's a QR code, append data
        if type == 'QRCODE':
            qr_code_data.append(data)

    # Break the loop if a QR code is found
    if qr_code_data:
        break

# When everything done, release the capture
cap.release()

# Return the text
print(''.join(qr_code_data))
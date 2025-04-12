import pyzbar.pyzbar as pyzbar
from PIL import Image
from typing import Union, List, Dict, Any, BinaryIO
import os.path
import io

def scan_qr_code(image_input: Union[str, Image.Image, bytes, BinaryIO]) -> List[Dict[str, Any]]:
    """
    Scan an image for QR codes and return the decoded information.

    Args:
        image_input: Either a file path to an image or a PIL Image object

    Returns:
        A list of dictionaries, each containing information about a QR code:
        - 'data': The decoded data (as UTF-8 string)
        - 'type': The type of barcode (e.g., 'QRCODE')
        - 'rect': The rectangle coordinates of the barcode
        - 'polygon': The polygon coordinates of the barcode

    Raises:
        FileNotFoundError: If the image path does not exist
        ValueError: If the image cannot be processed
        TypeError: If the input is neither a string path nor a PIL Image
    """
    # Handle different input types
    if isinstance(image_input, str):
        # Check if file exists
        if not os.path.isfile(image_input):
            raise FileNotFoundError(f"Image file not found: {image_input}")
        
        # Open the image file
        image = Image.open(image_input)
    elif isinstance(image_input, Image.Image):
        # Use the provided PIL Image object
        image = image_input
    elif isinstance(image_input, bytes):
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_input))
    elif hasattr(image_input, 'read'):
        # Handle file-like objects (including those from telebot)
        image = Image.open(image_input)
    else:
        raise TypeError("Input must be either a file path string, a PIL Image object, bytes, or a file-like object")
    
    # Decode all QR codes in the image
    decoded_objects = pyzbar.decode(image)
    
    # Format the results
    results = []
    for obj in decoded_objects:
        qr_data = {
            'data': obj.data.decode('utf-8'),
            'type': obj.type,
            'rect': obj.rect,
            'polygon': obj.polygon
        }
        results.append(qr_data)
    
    return results

# Example usage:
if __name__ == "__main__":
    # Example with file path
    try:
        file_path = "path/to/qr_code.png"
        results = scan_qr_code(file_path)
        print(f"Found {len(results)} QR code(s) in the image")
        for i, result in enumerate(results):
            print(f"QR Code {i+1}:")
            print(f"  Data: {result['data']}")
            print(f"  Type: {result['type']}")
    except Exception as e:
        print(f"Error: {e}")
        
    # Example with PIL Image
    try:
        # Create or load an image
        img = Image.open("path/to/another_qr.jpg")
        results = scan_qr_code(img)
        for result in results:
            print(f"Decoded QR data: {result['data']}")
    except Exception as e:
        print(f"Error: {e}")

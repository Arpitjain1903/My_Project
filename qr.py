import qrcode
import os
data="https://drive.google.com/file/d/1nrLGld1vv1pesxI4biwWxsfOiEzEibow/view?usp=sharing"
qr=qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=8,
    border=4,
)
qr.add_data(data)
qr.make(fit=True)

img=qr.make_image(fill_color="#d061f2",back_color="#f8f5fa")
img.save("qr1.png")
print("Qr code is successfully generated  and save as qr.png")

# import qrcode
# import os

# def create_local_image_qr(image_path, output_filename="local_image_qr.png"):
#     """
#     Create a QR code that opens a local image file when scanned
#     """
#     try:
#         # Convert to absolute path
#         abs_path = os.path.abspath(image_path)
        
#         # Create file:// URL for local file
#         file_url = f"file:///{abs_path.replace(os.sep, '/')}"
        
#         # Create QR code instance
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
        
#         # Add the file URL to QR code
#         qr.add_data(file_url)
#         qr.make(fit=True)
        
#         # Create QR code image
#         qr_image = qr.make_image(fill_color="#d061f2", back_color="#f8f5fa")
        
#         # Save the QR code
#         qr_image.save(output_filename)
#         print(f"✅ QR code generated successfully! Saved as: {output_filename}")
#         print(f"📁 Local image path: {abs_path}")
#         print(f"🔗 File URL: {file_url}")
#         print(f"📱 When scanned, this QR code will open the local image")
#         return True
        
#     except Exception as e:
#         print(f"❌ Error generating QR code: {e}")
#         return False

 
# # C:\Users\arpit\Desktop\photo.jpg
# IMAGE_PATH = r"D:\Users\arpit\Downloads\aryan11.jpg" # Change this path

# # Output filename for the QR code
# OUTPUT_FILENAME = "aryan11_qr.png"  # Change this if you want

# # ===== RUN THE PROGRAM =====
# if __name__ == "__main__":
#     print("=== QR Code for Local Image Generator ===")
#     print("This creates a QR code that opens a local image when scanned!")
    
#     # Check if file exists
#     if os.path.exists(IMAGE_PATH):
#         create_local_image_qr(IMAGE_PATH, OUTPUT_FILENAME)
#         print("🎉 QR code created successfully!")
#     else:
#         print(f"❌ File not found: {IMAGE_PATH}")
#         print("💡 Please update the IMAGE_PATH variable with the correct path to your image file.")
#         print("💡 Example: IMAGE_PATH = r'C:\\Users\\arpit\\Desktop\\my_photo.jpg'")






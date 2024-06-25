import streamlit as st
import pandas as pd
import qrcode
from PIL import Image
from io import BytesIO
import os
import zipfile

# Function to generate QR code
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

# Function to save QR code to BytesIO
def save_qr_to_bytesio(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# Function to create a zip file of all QR codes
def create_zip_file(file_list):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for file_name, file_data in file_list:
            zip_file.writestr(file_name, file_data.getvalue())
    zip_buffer.seek(0)
    return zip_buffer

# Streamlit UI
st.title("Bulk QR Code Generator")

uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.write("Columns in the uploaded file:")
    st.write(df.columns)

    if st.button("Generate QR Codes"):
        # Check for necessary columns
        required_columns = ['Name', 'DEG', 'Company Name', 'CTC', 'DOJ']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            st.error(f"Missing columns: {', '.join(missing_columns)}")
        else:
            file_list = []
            
            for index, row in df.iterrows():
                name = row['Name']
                data = f"Name: {row['Name']}\nDEG: {row['DEG']}\nCompany: {row['Company Name']}\nCTC: {row['CTC']}\nDOJ: {row['DOJ']}"
                qr_img = generate_qr_code(data)
                buffer = save_qr_to_bytesio(qr_img)
                
                file_list.append((f"{name}.png", buffer))

            # Create zip file
            zip_buffer = create_zip_file(file_list)
            
            # Provide download link for the zip file
            st.download_button(
                label="Download QR Codes as ZIP",
                data=zip_buffer,
                file_name="qr_codes.zip",
                mime="application/zip"
            )

            st.success("QR codes have been generated and are ready for download!")

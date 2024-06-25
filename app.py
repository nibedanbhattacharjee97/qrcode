import streamlit as st
import pandas as pd
import qrcode
from PIL import Image
from io import BytesIO
import os

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
            # Create 'output' directory if it doesn't exist
            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            for index, row in df.iterrows():
                name = row['Name']
                data = f"Name: {row['Name']}\nDEG: {row['DEG']}\nCompany: {row['Company Name']}\nCTC: {row['CTC']}\nDOJ: {row['DOJ']}"
                qr_img = generate_qr_code(data)
                buffer = save_qr_to_bytesio(qr_img)

                # Save the QR code image in the 'output' directory with the name from the 'Name' column
                with open(os.path.join(output_dir, f"{name}.png"), "wb") as f:
                    f.write(buffer.getvalue())

            st.success("QR codes have been generated and saved successfully!")

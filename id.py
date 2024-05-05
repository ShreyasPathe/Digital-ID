import streamlit as st
import csv
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

# Function to fetch student information from CSV file
def fetch_student_info(student_id):
    try:
        # Read data from CSV file
        with open('student.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['stuid']) == student_id:
                    return row
        return None
    except Exception as e:
        st.error(f"Error fetching student information: {e}")
        return None

# Function to send verification email with a random code
def send_verification_email(email, verification_code):
    try:
        # Set up SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Log in to your Gmail account
        server.login("idgenerator.vcet@gmail.com", "gajv vboa hhfz nefq")
        
        # Compose message
        msg = MIMEMultipart()
        msg['From'] = "idgenerator.vcet@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Verification Code for ID Card Generation"
        
        body = f"Your verification code is: {verification_code}"
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server.send_message(msg)
        
        # Close server connection
        server.quit()
        
        return True
    except Exception as e:
        st.error(f"Error sending verification email: {e}")
        return False

# Function to generate digital ID with QR code
def generate_digital_id(student_info):
    try:
        # Creating ID card image
        image = Image.new('RGB', (1000, 900), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        # College name
        x, y = 50, 50
        college_name = student_info.get("college", "Unknown")
        draw.text((x, y), college_name, fill=(0, 0, 0), font=font)

        # Student ID
        x, y = 50, 650
        student_id = student_info.get("stuid")
        draw.text((x, y), f"Student ID: {student_id}", fill=(0, 0, 0), font=font)

        # Full Name
        x, y = 50, 250
        full_name = student_info.get("name", "Unknown")
        draw.text((x, y), f"Name: {full_name}", fill=(0, 0, 0), font=font)

        # Gender
        x, y = 50, 350
        gender = student_info.get("gender", "Unknown")
        draw.text((x, y), f"Gender: {gender}", fill=(0, 0, 0), font=font)

        # Date of Birth
        x, y = 50, 450
        dob = student_info.get("dob", "Unknown")
        draw.text((x, y), f"Date of Birth: {dob}", fill=(0, 0, 0), font=font)

        # Age
        x, y = 250, 350
        age = student_info.get("age", "Unknown")
        draw.text((x, y), f"Age: {age}", fill=(0, 0, 0), font=font)

        # Blood Group
        x, y = 50, 550
        blood_group = student_info.get("bloodgroup", "Unknown")
        draw.text((x, y), f"Blood Group: {blood_group}", fill=(255, 0, 0), font=font)

        # Save ID card image
        image_file_name = f"{student_id}.png"
        image.save(image_file_name)

        # Generate QR code with student ID
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"DID: {student_id}")
        qr.make(fit=True)

        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image.save(f"{student_id}_qr.png")

        # Paste QR code onto the ID card image
        id_card_image = Image.open(image_file_name)
        qr_code_image = Image.open(f"{student_id}_qr.png")
        id_card_image.paste(qr_code_image, (600, 350))
        id_card_image.save(image_file_name)

        return image_file_name

    except Exception as e:
        st.error(f"Error generating digital ID: {e}")
        return None

# Function to generate and save OTP
def generate_and_save_otp():
    try:
        otp = str(random.randint(1000, 9999))
        with open('otp_cache.txt', 'w') as file:
            file.write(otp)
        return otp
    except Exception as e:
        st.error(f"Error generating OTP: {e}")
        return None

# Function to verify OTP
def verify_otp(user_otp):
    try:
        with open('otp_cache.txt', 'r') as file:
            otp = file.read()
            if otp == user_otp:
                return True
            else:
                return False
    except Exception as e:
        st.error(f"Error verifying OTP: {e}")
        return False

# Main function
def main():
    st.title("ID Card Generator")
    st.write("All Fields are Mandatory")
    st.write("Avoid any kind of Mistakes")

    # Example usage:
    student_id = st.text_input("Enter Student ID:")
    
    if st.button("Send Verification Email"):
        student_info = fetch_student_info(int(student_id))
        if student_info:
            email = student_info.get("email")
            if email:
                otp = generate_and_save_otp()
                if otp:
                    if send_verification_email(email, otp):
                        st.success("Verification email sent successfully.")
                    else:
                        st.error("Failed to send verification email.")
                else:
                    st.error("Failed to generate OTP.")
            else:
                st.error("Email not found in student information.")
        else:
            st.error("Student information not found.")
    
    verification_code = st.text_input("Enter Verification Code:")
    
    if st.button("Verify Email"):
        # Validate student ID and verification code
        try:
            student_id = int(student_id)
            student_info = fetch_student_info(student_id)
            if not student_info:
                st.error("Student information not found.")
                return
            
            if verify_otp(verification_code):
                digital_id_file = generate_digital_id(student_info)
                if digital_id_file:
                    digital_id_image = Image.open(digital_id_file)
                    st.image(digital_id_image, caption="Digital ID", use_column_width=True)

                    # Download button
                    st.download_button(label="Download ID", data=digital_id_file, file_name=digital_id_file, mime="image/png")
                else:
                    st.error("Failed to generate digital ID.")
            else:
                st.error("Verification code is invalid.")
        except ValueError:
            st.error("Invalid student ID. Please enter an integer.")
        except Exception as e:
            st.error(f"Error: {e}")

# Call the main function
if __name__ == "__main__":
    main()

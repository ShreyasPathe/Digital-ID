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
        # Generate QR code with student information
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(student_info['url'])
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        # Create digital ID image with student information
        digital_id = Image.new('RGB', (400, 600), color = (255, 255, 255))
        d = ImageDraw.Draw(digital_id)
        
        font = ImageFont.truetype('arial.ttf', size=20)
        
        d.text((10,10), f"Name: {student_info['name']}", font=font, fill=(0,0,0))
        d.text((10,40), f"Student ID: {student_info['stuid']}", font=font, fill=(0,0,0))
        d.text((10,70), f"Branch: {student_info['branch']}", font=font, fill=(0,0,0))
        d.text((10,100), f"College: {student_info['college']}", font=font, fill=(0,0,0))
        
        digital_id.paste(img, (50, 150))
        
        file_name = f"{student_info['stuid']}.png"
        digital_id.save(file_name)
        
        return file_name
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
                    st.success(f"Your Digital ID has been successfully created as '{digital_id_file}'")

                    # Download button
                    if os.path.exists(digital_id_file):
                        st.download_button(label="Download ID", data=digital_id_file, file_name=digital_id_file, mime="image/png")
                    else:
                        st.warning("Digital ID image not found.")
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

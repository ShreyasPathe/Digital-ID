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

# Function to generate digital ID
def generate_digital_id(student_info):
    # Digital ID generation code remains the same
    pass

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
                verification_code = str(random.randint(10000, 99999))
                if send_verification_email(email, verification_code):
                    st.success("Verification email sent successfully.")
                else:
                    st.error("Failed to send verification email.")
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
            
            # Check if the verification code matches the one stored in the CSV data
            stored_verification_code = student_info.get("verification_code")
            if not stored_verification_code:
                st.error("Verification code not found.")
                return
            
            if verification_code == stored_verification_code:
                generate_digital_id(student_info)
                st.success(f"Your Digital ID has been successfully created as '{student_id}.png'")

                # Download button
                if os.path.exists(f"{student_id}.png"):
                    st.download_button(label="Download ID", data=f"{student_id}.png", file_name=f"{student_id}.png", mime="image/png")
                else:
                    st.warning("Digital ID image not found.")
            else:
                st.error("Verification code does not match.")
        except ValueError:
            st.error("Invalid student ID. Please enter an integer.")
        except Exception as e:
            st.error(f"Error: {e}")

# Call the main function
if __name__ == "__main__":
    main()

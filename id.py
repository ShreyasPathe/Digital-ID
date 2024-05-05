import streamlit as st
import pymongo
import qrcode
from PIL import Image, ImageDraw, ImageFont
import datetime
import os
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["practicedb"]
students_collection = db["student"]

# Function to fetch student information from the database
def fetch_student_info(student_id):
    try:
        # Retrieve student information from the database
        student_info = students_collection.find_one({"stuid": int(student_id)})
        return student_info
    except Exception as e:
        st.error(f"Error fetching student information: {e}")
        return None

# Function to send verification email with a random code
def send_verification_email(student_id):
    try:
        # Fetch student information from the database
        student_info = fetch_student_info(student_id)
        if student_info:
            email = student_info.get("email")
            if email:
                # Generate random verification code
                verification_code = ''.join(random.choices('0123456789', k=5))

                # Store verification code in the database
                students_collection.update_one({"stuid": int(student_id)}, {"$set": {"verification_code": verification_code}})

                # Email configuration
                sender_email = "idgenerator.vcet@gmail.com"  # Replace with your email
                sender_password = "gajv vboa hhfz nefq"  # Replace with your password

                # Create message container
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = email
                msg['Subject'] = "Verify your identity"

                # Email body with verification code
                body = f"""We've received a request to create a digital ID associated with your email address.
        To proceed, please use the following verification code: **{verification_code}**.
        If you haven't initiated this process, kindly disregard this email."""


                # Attach body to the message
                msg.attach(MIMEText(body, 'plain'))

                # Create SMTP session
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)

                # Convert message to string
                text = msg.as_string()

                # Send email
                server.sendmail(sender_email, email, text)

                # Close SMTP session
                server.quit()

                st.success("Verification email sent successfully.")
            else:
                st.error("Email not found for the student.")
        else:
            st.error("Student information not found.")
    except Exception as e:
        st.error(f"Error sending verification email: {e}")

# Function to generate digital ID
def generate_digital_id(student_info):
    if not student_info:
        st.warning("Student information not found.")
        return

    try:
        # Creating ID card image
        image = Image.new('RGB', (1000, 900), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('arial.ttf', size=45)

        # College name
        x, y = 50, 50
        college_name = student_info.get("college", "Unknown")
        draw.text((x, y), college_name, fill=(0, 0, 0), font=font)

        # Student ID
        x, y = 650, 75
        student_id = student_info.get("stuid")
        draw.text((x, y), f"DID {student_id}", fill=(255, 0, 0), font=font)

        # Full Name
        x, y = 50, 250
        full_name = student_info.get("name", "Unknown")
        draw.text((x, y), full_name, fill=(0, 0, 0), font=font)

        # Gender
        x, y = 50, 350
        gender = student_info.get("gender", "Unknown")
        draw.text((x, y), gender, fill=(0, 0, 0), font=font)

        # Date of Birth
        x, y = 50, 450
        dob = student_info.get("dob", "Unknown")
        draw.text((x, y), dob, fill=(0, 0, 0), font=font)

        # Age
        x, y = 250, 350
        age = student_info.get("age", "Unknown")
        draw.text((x, y), f"{age}", fill=(0, 0, 0), font=font)

        # Blood Group
        x, y = 50, 550
        blood_group = student_info.get("bloodgroup", "Unknown")
        draw.text((x, y), blood_group, fill=(255, 0, 0), font=font)

        # Student ID
        x, y = 50, 650
        draw.text((x, y), str(student_id), fill=(0, 0, 0), font=font)

        # Address
        x, y = 50, 750
        address = student_info.get("add", "Unknown")
        draw.text((x, y), address, fill=(0, 0, 0), font=font)

        # Save ID card image
        image_file_name = f"{student_id}.png"
        image.save(image_file_name)

        # Generate QR code with student ID
        generate_qr_code_with_student_id(student_id)

        # Paste QR code onto the ID card image
        id_card_image = Image.open(image_file_name)
        qr_code_image = Image.open(f"{student_id}.jpg")
        id_card_image.paste(qr_code_image, (600, 350))
        id_card_image.save(image_file_name)

        st.image(image_file_name, caption='Generated Digital ID', use_column_width=True)

    except Exception as e:
        st.error(f"Error generating digital ID: {e}")

def generate_qr_code_with_student_id(student_id):
    try:
        # Fetch student information from the database using the student_id
        student_info = fetch_student_info(student_id)
        if not student_info:
            raise ValueError("Student information not found")

        # Get the URL from the student information
        url = student_info.get("url")
        if not url:
            raise ValueError("URL not found in student information")

        # Create a QR code with the image URL
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code image as a file
        qr_img.save(f"{student_id}.jpg")

    except Exception as e:
        st.error(f"Error generating QR code: {e}")

# Main function
def main():
    st.title("ID Card Generator")
    st.write("All Fields are Mandatory")
    st.write("Avoid any kind of Mistakes")

    # Example usage:
    student_id = st.text_input("Enter Student ID:")
    
    if st.button("Send Verification Email"):
        student_info = fetch_student_info(student_id)
        if student_info:
            email = student_info.get("email")
            if email:
                send_verification_email(student_id)
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
            
            # Check if the verification code matches the one stored in the database
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

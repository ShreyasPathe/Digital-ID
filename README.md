# ID Generator Project

This project, titled **ID Generator**, uses Streamlit to create a web application that generates IDs based on input from a CSV file. The application integrates functionalities like QR code generation, Time-based One-Time Passwords (TOTP), and image processing.

## Project Overview
The ID Generator project is designed to streamline the process of generating unique IDs for individuals listed in a CSV file. It leverages the power of Streamlit for the web interface and integrates several key libraries to enhance functionality.

### Features
- **Streamlit Web App**: An interactive interface for uploading CSV files and generating IDs.
- **QR Code Generation**: Creates QR codes for each ID using the `qrcode` library.
- **TOTP Generation**: Implements Time-based One-Time Passwords using the `pyotp` library.
- **Image Processing**: Utilizes the `Pillow` library for image handling and manipulation.

## Installation and Setup
To run this project, you need to have Python and Streamlit installed on your machine. Follow these steps to get started:

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/id-generator.git
   cd id-generator
   ```

2. **Install the required libraries**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**:
   ```bash
   streamlit run id_generator.py
   ```

## Libraries Used
- **Streamlit**: For building the interactive web app.
- **Pandas**: For data manipulation and analysis.
- **qrcode**: For generating QR codes.
- **pyotp**: For generating Time-based One-Time Passwords (TOTP).
- **Pillow (PIL)**: For image processing.

## Dataset
The project takes input from a CSV file. The CSV file should contain relevant details required for generating IDs. An example format of the CSV file is as follows:

```csv
name,email,phone
John Doe,johndoe@example.com,1234567890
Jane Smith,janesmith@example.com,0987654321
```

## Usage
1. **Launch the Streamlit app using the command mentioned above**.
2. **Upload your CSV file** containing the details for which IDs need to be generated.
3. **The app will process the data** and generate IDs, along with QR codes and TOTP.
4. **Download the generated IDs and QR codes** directly from the app.

## Project Structure
- `id_generator.py`: Main script to run the Streamlit app.
- `requirements.txt`: List of required libraries.

## Example Code
Here's a snippet of the main parts of the project:

```python
import streamlit as st
import pandas as pd
import qrcode
import pyotp
from PIL import Image

# Title
st.title('ID Generator')

# Upload CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data)

    for index, row in data.iterrows():
        name = row['name']
        email = row['email']
        phone = row['phone']

        # Generate QR code
        qr = qrcode.make(f'Name: {name}\nEmail: {email}\nPhone: {phone}')
        qr_image = f'{name}_qrcode.png'
        qr.save(qr_image)

        # Display QR code
        st.image(qr_image, caption=f'{name} QR Code')

        # Generate TOTP
        totp = pyotp.TOTP(pyotp.random_base32())
        st.write(f'{name} TOTP: {totp.now()}')
```

## Acknowledgements
I would like to thank everyone who contributed to this project and provided valuable feedback during the development process.

---

Feel free to contribute to this project by forking the repository and submitting pull requests. If you encounter any issues, please open an issue on GitHub.

---

**Disclaimer**: This project is for educational purposes only. The dataset and models used are simplified and may not reflect real-world complexities.

---

For more information, please visit [GitHub](https://github.com/yourusername/id-generator).
```

### `requirements.txt`
Make sure to include this `requirements.txt` file in your repository:

```plaintext
streamlit
pandas
qrcode
pyotp
Pillow
```

### Notes
- Replace `yourusername` with your actual GitHub username in the URLs.
- Ensure that the example code snippet provided matches the structure and functionality of your actual `id_generator.py` script.
- If there are additional instructions or dependencies, update the `README.md` accordingly.

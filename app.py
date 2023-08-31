from flask import Flask, render_template, request, redirect, url_for, session
import qrcode
from io import BytesIO
import base64
import pyotp

app = Flask(__name__)
app.secret_key = 'your_secret_key' 


@app.route('/')
def display_form():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        age = request.form['age']

        # Generate QR code and OTP secret key
        key = pyotp.random_base32()
        totp = pyotp.TOTP(key)
        uri = totp.provisioning_uri(name=name, issuer_name="2FA CyberGritt")
        img = qrcode.make(uri)
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

        # Store user details in session
        session['user_details'] = {
            'name': name,
            'email': email,
            'phone': phone,
            'address': address,
            'age': age,
        }

    return render_template('registration_success.html', img_base64=img_base64, secret_key=key)


@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    if request.method == 'POST':
        secret_key = request.args.get('secret_key')  # Get secret_key from URL parameters
        user_otp = request.form['otp']
        totp = pyotp.TOTP(secret_key)
        is_valid = totp.verify(user_otp)

        if is_valid:
            return "success"
        else:
            return "failure"

@app.route('/success_page')
def success_page():
    return render_template('success_page.html')

if __name__ == '__main__':
    app.run(debug=True)

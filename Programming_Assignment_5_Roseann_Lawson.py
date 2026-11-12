# Roseann Lawson
# CIS256 Fall 2026
# Programming Assignment 5

from flask import Flask, request
import bcrypt
import re

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():

    # Display registration form
    if request.method == 'GET':
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Registration Form</title>
        </head>
        <body>
            <h2>User Registration</h2>

            <form method="POST">

                <label>Full Name:</label><br>
                <input type="text" name="fullname" required><br><br>

                <label>Username:</label><br>
                <input type="text" name="username" required><br><br>

                <label>Password:</label><br>
                <input type="password" name="password" required><br><br>

                <label>Confirm Password:</label><br>
                <input type="password" name="confirm_password" required><br><br>

                <input type="submit" value="Register">

            </form>

        </body>
        </html>
        '''

    # Capture submitted form data
    fullname = request.form.get("fullname")
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    errors = []

    # Username validation
    if not re.match(r'^\w+$', username):
        errors.append(
            "Username may only contain letters, numbers, and underscores."
        )

    # Password length validation
    if len(password) < 8:
        errors.append(
            "Password must be at least 8 characters long."
        )

    # Password letter validation
    if not re.search(r'[A-Za-z]', password):
        errors.append(
            "Password must contain at least one letter."
        )

    # Password number validation
    if not re.search(r'[0-9]', password):
        errors.append(
            "Password must contain at least one number."
        )

    # Confirm passwords match
    if password != confirm_password:
        errors.append(
            "Password and Confirm Password do not match."
        )

    # Display errors if any validation fails
    if errors:
        error_html = "<br>".join(errors)

        return f'''
        <html>
        <body>

            <h2>Registration Error</h2>

            <p style="color:red;">
                {error_html}
            </p>

            <a href="/register">Return to Registration Form</a>

        </body>
        </html>
        '''

    # Hash password using bcrypt
    password_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(
        password_bytes,
        salt
    )

    hashed_password = hashed_password.decode('utf-8')

    # Successful registration message
    return f'''
    <html>
    <body>

        <h2>Registration Successful!</h2>

        <p>
            <strong>Full Name:</strong>
            {fullname}
        </p>

        <p>
            <strong>Username:</strong>
            {username}
        </p>

        <p>
            <strong>Hashed Password:</strong>
        </p>

        <p>
            {hashed_password}
        </p>

        <a href="/register">Register Another User</a>

    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=5002)
    print(app.url_map)
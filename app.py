from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import datetime
import os

app = Flask(__name__)
app.secret_key = 'flash message'  # Secret key for session management and flash messages
app.secret_key = os.urandom(24)

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'Your_Email'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'Your_Apppasswords'   # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'Sender_Email'
mail = Mail(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'flaskuser'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'student_management'
mysql = MySQL(app)

# Route for the login page (index)
@app.route('/')
def index():
    return render_template('index.html')  # Render the login page

# Route for the home page, accessible after login
@app.route('/home')
def home():
    if 'user_id' in session:  # Check if user is logged in
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM students_info')  # Fetch student data
        data = cur.fetchall()
        cur.close()
        return render_template('home.html', students_info=data)  # Render home page with student data
    else:
        flash('You must login to access this page.', 'error')
        return redirect(url_for('login'))  # Redirect to login if not logged in

# Route to handle data insertion
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students_info (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.connection.commit()
        cur.close()
        flash('Data inserted successfully')  # Flash message for successful insertion
        return redirect(url_for('home'))  # Redirect to home page

# Route to handle data update
@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute('''
            UPDATE students_info
            SET name=%s, email=%s, phone=%s
            WHERE id=%s
        ''', (name, email, phone, id_data))
        mysql.connection.commit()
        cur.close()
        flash('Data Updated Successfully')  # Flash message for successful update
        return redirect(url_for('home'))  # Redirect to home page

# Route to handle data deletion
@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM students_info WHERE id = %s', (id_data,))
    mysql.connection.commit()
    cur.close()
    flash('Data Deleted Successfully')  # Flash message for successful deletion
    return redirect(url_for('home'))  # Redirect to home page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')  # Changed from 'email' to 'username'
        password = request.form.get('password')

        if not username or not password:
            flash('Username and Password are required!', 'danger')
            return redirect(url_for('login'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if user:
            stored_password_hash = user[2]  # Assuming password is in the 3rd column
            if check_password_hash(stored_password_hash, password):
                session['user_id'] = user[0]  # Set user session
                flash('Login successful!', 'success')
                return redirect(url_for('home'))  # Redirect after successful login
            else:
                flash('Invalid username or password!', 'error')
        else:
            flash('Invalid username or password!', 'error')

        cur.close()

    return render_template('index.html')


# Route to handle user logout
@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    flash('You have been logged out successfully.', 'success')  # Flash success message for logout
    return redirect(url_for('index'))  # Redirect to login page


# Route for requesting password reset
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        if user:
            # Generate token and expiration time
            token = secrets.token_urlsafe(16)
            expiration = datetime.datetime.now() + datetime.timedelta(hours=1)
            cur.execute("UPDATE users SET reset_token = %s, token_expiration = %s WHERE email = %s", (token, expiration, email))
            mysql.connection.commit()

            # Send reset email
            reset_link = url_for('reset_with_token', token=token, _external=True)
            msg = Message('Password Reset Request', recipients=[email])
            msg.body = f'Click here to reset your password: {reset_link}'
            mail.send(msg)

            flash('Password reset link sent! Please check your email.', 'success')
        else:
            flash('Email not found!', 'danger')
        cur.close()
        return redirect(url_for('reset_password'))

    return render_template('reset_password.html')

# Route for resetting password with token
@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE reset_token = %s", (token,))
    user = cur.fetchone()

    if not user:
        flash('Invalid or expired token!', 'danger')
        return redirect(url_for('reset_password'))

    # Fetch token_expiration from the database
    token_expiration = user[5]  # Assuming the expiration is stored in the 6th column

    # Ensure token_expiration is a datetime object
    if isinstance(token_expiration, str):
        # Convert the string to datetime if it's not in the correct format
        try:
            token_expiration = datetime.datetime.strptime(token_expiration, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            flash('Invalid token expiration format!', 'danger')
            return redirect(url_for('reset_password'))

    # Compare token expiration to the current time
    if token_expiration < datetime.datetime.now():
        flash('Token expired! Please request a new one.', 'danger')
        return redirect(url_for('reset_password'))

    # Handle POST request to reset the password
    if request.method == 'POST':
        new_password = request.form['password']
        hashed_password = generate_password_hash(new_password)  # Hash the new password

        # Update the password and clear the token and expiration
        cur.execute("UPDATE users SET password = %s, reset_token = NULL, token_expiration = NULL WHERE reset_token = %s", (hashed_password, token))
        mysql.connection.commit()
        cur.close()

        flash('Your password has been reset! Please log in.', 'success')
        return redirect(url_for('login'))

    cur.close()
    return render_template('reset_with_token.html', token=token)



# Run the application
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader
(template_dir))
app = Flask(__name__)
app.config['DEBUG'] = True



@app.route('/')
def display_user_form():
    template = jinja_env.get_template('user_form.html')
    return template.render()

def is_string(text):
    try:
        str(text)
        return True
    except TypeError:
        return False

@app.route('/', methods=['POST'])
def validate_user():

    user = request.form['user']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    user_error = ''
    password_error = ''
    verify_error = ''
    email_error = ''

    if not is_string(user):
        user_error = "Not a valid username"
    else:
        user = str(user)
        if ' ' in user:
            user_error = "Not a valid username"
    
    if not is_string(password):
        password_error = "Not a valid password"
    
    elif ' ' in password:
        password_error = "Not a valid password"
    else:
        password = str(password)
        if len(password) < 3 or len(password) > 19:
            password_error = "Password out of range(3-20)"
    if not is_string(email):
        email_error = "Not a valid email"
    else:
        email = str(email)
        if "@" not in email or "." not in email:
            email_error = "Not a valid email"

    if not is_string(verify):
        verify_error = "Not a valid password"
    else:
        verify = str(verify)
        if verify != password:
            verify_error = "Password does not match"


    if not password_error and not verify_error and not email_error and not user_error:
        return "Welcome, " + user

    else:
        template = jinja_env.get_template('user_form.html')
        return template.render(user=user, password=password, password_error=password_error, 
        verify=verify, verify_error=verify_error, email=email, email_error=email_error, user_error=user_error,)

app.run()
from flask import Flask, session, redirect, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from forms import LoginForm, RegistrationForm, SubscribeForm
from flask_sqlalchemy import SQLAlchemy
import smtplib # for email subscription
import bcrypt # for password encryption

app = Flask(__name__)

# default route (Homepage)
@app.route('/')
def index():
    return render_template('Home.html', username=session.get('username'))

@app.route('/More_Characters')
def moreCharacters():
    return render_template('More_Characters.html')

@app.route('/Fanart')
def fanart():
    return render_template('Fanart.html')

@app.route('/Contact')
def contact():
    return render_template('Contact.html')

@app.route('/Subscribe', methods=['GET','POST'])
def subscribe():
    form = SubscribeForm() # creating an instance of SubscribeForm
    if form.validate_on_submit():

      # The message that will be sent in the email
      message = "Thank you for visiting the One Piece Character Introduction Site! You have successfully been subscribed to the newsletter and will receive updates on One Piece."
      # Creating the gmail server
      server = smtplib.SMTP("smtp.gmail.com", 587)
      server.starttls()
      # The gmail account that will be used to send the email (email and password to log in)
      server.login("flaskpython0628@gmail.com", "PASSWORD")
      words = 'Subject: {}\n\n{}'.format('One Piece Newsletter', message)
      server.sendmail("flaskpython0628@gmail.com", form.email.data, words)
      server.quit()
      flash('Thank you {} for subscribing to the newsletter! An email has been sent to your account'.format(form.name.data), 'success')
      return redirect('/Subscribe')
    return render_template('Subscribe.html', form=form)

app.secret_key = '00b380248078448d851f0485d9f6d187' # secret key generated using python os
login_manager = LoginManager()
login_manager.init_app(app)
# without setting the login_view, attempting to access @login_required endpoints will result in an error
# this way, it will redirect to the login page
login_manager.login_view = 'login'
app.config['USE_SESSION_FOR_NEXT'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = r"sqlite:///data/userInfo.sqlite" # database file
db = SQLAlchemy(app)

# database class for User model (creating a table)
class DBUser(db.Model):
  __tablename__ = 'users'
  username = db.Column(db.Text(), primary_key=True)
  email = db.Column(db.Text(), nullable=False)
  phone = db.Column(db.Text())
  password = db.Column(db.Text(), nullable=False)

  def __repr__(self):
    return "<User {}: {} {}>".format(self.username, self.email, self.phone)



# User parametrized constructor
class SessionUser(UserMixin):
    def __init__(self, username, email, phone, password=None):
        self.id = username
        self.email = email
        self.phone = phone
        self.password = password

# this is used by flask_login to get a user object for the current user
@login_manager.user_loader

def load_user(user_id):
    user = find_user(user_id)
    if user:
        # Hiding the password if there is a User
        user.password = None

    return user

# searching through the database to find the corresponding user with the same username as the input and returning
# that user
def find_user(username):
  user = DBUser.query.filter_by(username=username).first()
  if user:
    user = SessionUser(user.username, user.email, user.phone, user.password)
  return user


@app.route('/Login', methods=['GET', 'POST'])
def login():
    form = LoginForm() # Creating a new instance of a LoginForm

    if form.validate_on_submit(): # When the user clicks the login button
        user = find_user(form.username.data) # Finding the user with the corresponding username in the database

        if user and bcrypt.checkpw(form.password.data.encode(), user.password.encode()):
          # Using the bcrypt algorithm since the passwords are kept in hashed form
            login_user(user)

            # check if the next page is set in the session by the @login_required decorator
            # if not set, it will default to '/'
            next_page = session.get('next', '/')
            # reset the next page to default '/'
            session['next'] = '/'
            flash('You have been logged in', 'success')
            return redirect(next_page)
        else:
            flash('Incorrect username or password! Please try again', 'danger')
    return render_template('Login.html', form=form)

# Occurs when user clicks the logout button. It redirects you back to the homepage
@app.route('/Logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm() # Creating an instance of RegistrationForm

    if form.validate_on_submit(): # When the user clicks the Register button

        user = find_user(form.username.data)# First check if username already exists

        # If the user enters a new unique username that is not in the database
        if not user:
            # The bcrypt algorithm to hash the password
            hashing = bcrypt.gensalt()
            password = bcrypt.hashpw(form.password.data.encode(), hashing)
            # Creating the new user
            user = DBUser(username=form.username.data, email=form.email.data, phone=form.phone.data,
                          password=password.decode())
            # Adding the new created user into the database
            db.session.add(user)
            db.session.commit()
            flash('Registered successfully.', 'success')
            return redirect('/Login')
        # If the user enters a username that already exists in the database
        else:
            flash('This username already exists, choose another one')
    return render_template('Registration.html', form=form)

@app.route('/users', methods=['GET'])
@login_required
def other_users():
    # Getting all the users in the database
    users = DBUser.query.all()
    return render_template('Users.html',
                           users=users,
                           title="Show Users")

if __name__ == '__main__':
    app.run()





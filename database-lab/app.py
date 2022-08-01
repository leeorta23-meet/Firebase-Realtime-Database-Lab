from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
  "apiKey": "AIzaSyAZGOF5MSb-dNb9IcZmJgEKaHhWtzZhbqg",
  "authDomain": "fir-lab-aa8fe.firebaseapp.com",
  "projectId": "fir-lab-aa8fe",
  "storageBucket": "fir-lab-aa8fe.appspot.com",
  "messagingSenderId": "220786561707",
  "appId": "1:220786561707:web:faf8886bb5286efeb15dee",
  "measurementId": "G-MTZEX6CV6N",
  "databaseURL": "https://twitter-56dc7-default-rtdb.europe-west1.firebasedatabase.app/"}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
            return render_template("signin.html")
    else:        
        return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']
        uid = login_session['user']['localId']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)

            user = {"email": request.form['email'], "password":request.form['password'], 
            "full_name": request.form['full_name'], "username":request.form['username'], "bio": request.form['bio']}
            
            db.child("Users").child(login_session['user']['localId']).set(user)

            return redirect(url_for('add_tweet'))
        except:
           error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error = ""
    if request.method == 'POST':
        title = request.form["title"]
        text = request.form["text"]
        try:
   
            tweet = {"title": request.form['title'], "text":request.form['text'], "uid": login_session['user']['localId']}
            db.child("Tweets").child(login_session['user']['localId']).push(tweet)

            return redirect(url_for('add_tweet'))
        except:
           error = "Authentication failed"
    return render_template("add_tweet.html")

@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():


if __name__ == '__main__':
    app.run(debug=True)
import os

from flask import Flask, redirect, url_for, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import requests

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Create a decorator (helper function for @app.route) that requires the user to log in at specified pages
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Landing page is the sign up page
@app.route("/", methods=["GET", "POST"])
def signup():
    # if users got to the page by "GET", then just offer him to sign up
    if request.method == "GET":
        return render_template("signup.html")
    # if POST, the user must have submitted the signup form, and INSERT his entry to the database.
    else: 
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("user_email")
        # using werkzeug.security library we hash the password before storing it
        password = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users(fname, lname, email, passwd) VALUES (:fname, :lname, :email, :passwd)", 
            {"fname": fname, "lname": lname, "email": email, "passwd": password})
        db.commit()
        # once data is inserted, redirect the user to the login page
        return redirect(url_for('login'))

# login page
@app.route("/login", methods=["GET", "POST"])
def login():
    # when the route is loaded, we clean the session from previous user information
    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    # if POST, then user must have enterd log in information
    else:
        # fetch the entries from the forms
        email = request.form.get("l_user_email")
        psw = request.form.get("l_password")
        # try finding the email in the database
        try:
            user_info = db.execute("SELECT * FROM users WHERE email= :email", {"email": email}).fetchone()
        except:
            return "Error While Fetching Data by Email"
        
        # if user_info did not fetch anything, then there is no such email
        if user_info is None:
            return "Email Not Found"

        # check if the entered password mathes the one on file, using werkzeug.security library
        passwdr = user_info.passwd
        if check_password_hash(passwdr, psw) == False:
            return "The entered password does not match"

        # After all precautions, we 'log' the use in by storing his data on the session
        session["fname"] = user_info.fname
        session["lname"] = user_info.lname
        session["email"] = user_info.email
        session["id"] = user_info.user_id
        session["logged_in"] = True

        # redirect the user to the search page
        return redirect(url_for("libby"))

# search page
@app.route("/libby", methods=["GET", "POST"])
@login_required
def libby():
    if request.method == "GET":
        return render_template("libby.html")
    # If POST, then user must have submitted a query
    else:
        # Fetch the query from the form
        query = request.form.get("lsearch")
        # Query the database for the user's search
        result = db.execute("SELECT * FROM books WHERE title ILIKE :query OR isbn ILIKE :query OR author ILIKE :query", {"query": "%" + query + "%"}).fetchall()
        # if nothing found, return "Nothing Found"
        if not result:
            return "Nothing matched your search"
        # return the page with the results of the search
        return render_template("libby.html", result=result)

# page for every book
@app.route("/libby/<string:isbn>", methods=["GET", "POST"])
@login_required
def book(isbn):
    # Get all the information for the book's page
    result = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    # Use Goodreads API to get average_rating and work_rating_count, as well as many other variables
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "MZfmUkTuocX88glHuG9wOg", "isbns": "9781632168146"})
    data = res.json()
    average = data['books'][0]['average_rating'] 
    num_of_ratings = data['books'][0]['work_ratings_count']
    # Get all the reviews that users left for the book on the website
    reviews = db.execute("SELECT * FROM reviews WHERE book_isbn= :isbn", {"isbn": isbn}).fetchall()
    return render_template("book.html", isbn=result.isbn, title=result.title, author=result.author, year=result.year, average=average, num_of_ratings=num_of_ratings, reviews=reviews)

# this route serves as a function that check if the user has already left the review and allows him to do so if not
@app.route("/libby/<string:isbn>/submit", methods=["POST"])
@login_required
def submit(isbn):
    rating = request.form.get("rating")
    review = request.form.get("comment")
    # Return the statement if user has already left a review for the book
    result = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_isbn = :isbn", {"user_id": session['id'], "isbn": isbn}).fetchone()
    if result:
        return "You have already rated and reviewed this book"
    
    # If user has not left review, insert his review in the database and commit changes
    db.execute("INSERT INTO reviews(book_isbn, comment, rating, user_id) VALUES (:isbn, :comment, :rating, :user_id)", {"isbn": isbn, "comment": review, "rating": rating, "user_id": session['id']})
    db.commit()
    # Redirect the user back to the book's page
    return redirect(url_for("book", isbn=isbn))

# route for loggin out the user
@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))

# API route
@app.route("/api/<string:isbn>")
def api(isbn):
    # Get all the data required for the API
    result = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "MZfmUkTuocX88glHuG9wOg", "isbns": "9781632168146"})
    data = res.json()
    average = data['books'][0]['average_rating'] 
    num_of_ratings = data['books'][0]['work_ratings_count']
    # Jsonify the data to present it in JSON format
    return jsonify({
            "title": result.title,
            "author": result.author,
            "year": result.year,
            "isbn": result.isbn,
            "review_count": num_of_ratings,
            "average_score": average
    })

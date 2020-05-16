# Book Reviews

## Overview

The website features 5000 books that are stored on the PostgreSQL database. Users can look up and review the books, as well as read general information and reviews from other users. The application utilizes the Goodreads API for fetching extra information. Also, the web application offers its own API.

## Overview Video

[![IMAGE ALT TEXT HERE](https://img.https://youtu.be/vi/n3IWYhftpbE/0.jpg)](https://youtu.be/n3IWYhftpbE)

## Features

* **Registration**: Users are able to register for the website, providing first and last names, a username and password.
* **Login**: Users, once registered, are able to log into website with their username and password.
* **Logout**: Logged in users are able to log out of the site.
* **Import**: From books.csv, import.py imports the data entries into PostgreSQL according to the ERD in db-books-ERD.png
![Alt text](db-books-ERD.png?raw=true "Title")
* **Search**: Once a user has logged in, they are be taken to a page where they can search for a book. Users are able to type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, the website displays a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name, the search page finds matches for those as well!
* **Book Page**: When users click on a book from the results of the search page, they are be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on the website.
* **Review Submission**: On the book page, users are able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users should are not able to submit multiple reviews for the same book.
* **Goodreads Review Data**: The book page also displays (if available) the average rating and number of ratings the work has received from Goodreads.
* **API Access**: If users make a GET request to the website’s `/api/<isbn>` route, where <isbn> is an ISBN number, the website returns a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. For example:
``` json
{
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2015,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
}
```

## Proceed to download

1. Clone the repository
2. In your terminal window, navigate into the project
3. Run `pip install -r requirements.txt` to installe the necessary Python packages
4. Set the environment variables:
	  * `set FLASK_APP=application.py`
      * `set DATABASE_URL="link or path to yor database`
    - `KEY` = is your API key, will give you the review and rating data for the book with the provided ISBN number (register at goodreads.com)
5. Run `create.sql` against your database to create the necessary tables

6. Run `python import.py` to import a spreadsheet in CSV format of 5000 different books to your database
7. Finally execute `flask run` command in your terminal to start the server

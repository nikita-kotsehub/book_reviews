-- This file contains SQL commands that create the database's tables
CREATE TABLE books (
    isbn VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    fname VARCHAR NOT NULL,
    lname VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    passwd VARCHAR NOT NULL
);

CREATE TABLE reviews (
    book_isbn VARCHAR REFERENCES books(isbn),
    user_id SERIAL REFERENCES users(user_id),
    rating INTEGER CONSTRAINT invalid_rating CHECK (rating >=1 AND rating <= 5),
    comment VARCHAR 
);
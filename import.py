import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    # open the cvs file
    file = open("books.csv") 
    # read the file and skip the first entry, which is the column names
    reader = csv.reader(file)
    next(reader)

    for isbn, title, author, year in reader:
        # for each entry, insert the values into the database and commit the changes
        db.execute("INSERT INTO books(isbn, title, author, year) VALUES(:isbn, :title, :author, :year)", 
            {"isbn": isbn, "title": title, "author": author, "year": year})
        db.commit()
        print(f"Added book {isbn}, {title}, {author}, {year}.")
    
if __name__ == "__main__":
    main()


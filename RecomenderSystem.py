
#Recommendation system based on ratings of a movie

import csv
import sqlite3
from prettytable import PrettyTable

database = sqlite3.connect("Movies.db")
db = database.cursor()


# Method to convert the give CSV files into database.
def createdatabase():
    db.execute(
        "CREATE TABLE IF NOT EXISTS links (movieId INTEGER, imdbId INTEGER, tmdbId INTEGER);")
    reader = csv.DictReader(open('links.csv', 'r'), delimiter=',')
    for row in reader:
        to_db = [row['movieId'].encode('utf-8'), row['imdbId'].encode('utf-8'), row['tmdbId'].encode('utf-8')]
        db.execute("INSERT INTO links (movieid, imdbid, tmdbid) VALUES (?, ?, ?);", to_db)
    database.commit()

    db.execute(
        "CREATE TABLE IF NOT EXISTS movies (movieId INTEGER, title VARCHAR, genres VARCHAR);")
    reader = csv.DictReader(open('movies.csv', 'r'), delimiter=',')
    for row in reader:
        to_db = [row['movieId'].encode('utf-8'), row['title'].encode('utf-8'),
                 row['genres'].replace('|', ',').encode('utf-8')]
        db.execute("INSERT INTO movies (movieid, title, genres) VALUES (?, ?, ?);", to_db)
    database.commit()

    db.execute(
        "CREATE TABLE IF NOT EXISTS ratings (userId INTEGER, movieId INTEGER, rating FLOAT, timestamp INTEGER);")
    reader = csv.DictReader(open('ratings.csv', 'r'), delimiter=',')
    for row in reader:
        to_db = [row['userId'].encode('utf-8'), row['movieId'].encode('utf-8'), row['rating'].encode('utf-8'),
                 row['timestamp'].encode('utf-8')]
        db.execute("INSERT INTO ratings (userId, movieId, rating, timestamp) VALUES (?, ?, ?, ?);", to_db)
    database.commit()

    db.execute(
        "CREATE TABLE IF NOT EXISTS tags (useriD INTEGER, movieId INTEGER, tag VARCHAR, timestamp INTEGER);")
    reader = csv.DictReader(open('tags.csv', 'r'), delimiter=',')
    for row in reader:
        to_db = [row['userId'].encode('utf-8'), row['movieId'].encode('utf-8'), row['tag'].encode('utf-8'),
                 row['timestamp'].encode('utf-8')]
        db.execute("INSERT INTO tags (userId, movieId, tag, timestamp) VALUES (?, ?, ?, ?);", to_db)
    database.commit()


#Menu for recommendation
def Recom():
    typ = input("Enter Recommendation Type.\n1.Based on name\n2.Genre based.\n")
    if typ == '1':
        mName = input("Enter Movie name or keyword: \n")
        nameRecom(mName)
    elif typ == '2':
        genreRecom()
    else:
        print("Incorrect option. Please select correct option.")


#Method to recommend based on movie name or a keyword
def nameRecom(mName):
    mName = str("%" + mName + "%")
    db.execute(
        "SELECT movies.movieId,title,genres,avg(rating) AS Rating FROM movies,ratings WHERE movies.title LIKE ? AND movies.movieId = ratings.movieId GROUP BY title ORDER BY Rating DESC;",
        [mName])
    mList = db.fetchall()
    print("List of Movies based on give name in order of ratings :\n")
    table = PrettyTable(['MovieId', 'Movie Name', 'Genre', 'Rating'])
    for record in mList:
        table.add_row([record[0].decode('utf-8'), record[1].decode('utf-8'), record[2].decode('utf-8'), record[3]])
    table.align = 'l'
    print(table)


#Method to recomend based on genre
def genreRecom():

    # getting all the distinct genres
    genrelist = []
    for row in db.execute("SELECT DISTINCT genres FROM movies"):
        for name in row[0].decode('utf-8').split(','):
            genrelist.append(name)
    gset = set(genrelist)
    for genre in gset:
        print(genre, end=",")

    #Taking the user input for the liked genres
    gList = str(input("\nEnter movie genre followed by ',' from the given list(case sensitive) :\n")).strip().split(
        ',')
    GMList = []
    for genre in gList:
        genre = str("%" + genre + "%")
        for row in db.execute(
                "SELECT movies.movieId,title,genres,avg(rating) AS Rating FROM movies,ratings WHERE genres LIKE ? AND movies.movieId = ratings.movieId GROUP BY title ORDER BY Rating DESC;",
                [genre]):
            if row in GMList:
                pass
            else:
                GMList.append(row)

    table = PrettyTable(['MovieId', 'Movie Name', 'Genre', 'Rating'])
    for record in GMList:
        for g in gList:
            if g in record[2].decode('utf-8').split(','):
                flag = True
            else:
                flag = False
                break  # Comment out this break to include other movies with not all the genre
        if flag:
            table.add_row(
                [record[0].decode('utf-8'), record[1].decode('utf-8'), record[2].decode('utf-8'), record[3]])
    table.align = 'l'
    print(table)

#main Fuction
if __name__ == '__main__':
    createdatabase()
    while True:
        Recom()
        print("Search Another Movie: \n")

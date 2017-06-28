import sqlite3 as sql
import pandas as pd
import numpy as np
import csv

db = sql.connect('movies.db')
c = db.cursor()

c.execute('''
        CREATE TABLE movies(
        movieID integer,
        title text,
        genres text
        )
        ''')
    
c.execute('''
        CREATE TABLE ratings(
        userID integer,
        movieID integer,
        rating real,
        timestamp integer
        )''')

c.execute('''
        CREATE TABLE tags(
        userID integer,
        movieID integer,
        tag text,
        timestamp text
        )''')
        
with open('movies.csv') as file:
    mvs = csv.reader(file, delimiter=',')
    for row in mvs:
        c.execute('''
        insert into movies VALUES(?,?,?)''', (row[0], row[1], row[2]))
        
with open('tags.csv') as file:
    tgs = csv.reader(file, delimiter=',')
    for row in tgs:
        c.execute('''
        insert into tags VALUES(?,?,?,?)''', (row[0], row[1], row[2], row[3]))
        
with open('ratings.csv') as file:
    rts = csv.reader(file, delimiter=',')
    for row in rts:
        c.execute('''
        insert into ratings VALUES(?,?,?,?)''', (row[0], row[1], row[2], row[3]))

db.commit()

#top 5 rated
query1 = '''
        SELECT title, AVG(rating) as a
        FROM ratings as r
        JOIN movies as m ON m.movieId = r.movieId
        
        GROUP BY title
        
        ORDER BY a DESC
        LIMIT 5
        '''
top = pd.read_sql(query1, con=db)
top.to_csv('top.csv')


#titanic
query2 = '''
        SELECT userId, rating
        FROM ratings as r
        WHERE movieId = 1721 AND rating != 5.0
        '''
titanic = pd.read_sql(query2, con=db)
titanic.to_csv('titanic.csv')

#common_tag
query3 = '''
        SELECT title
        FROM movies
        WHERE movies.movieId IN (
            SELECT movieId
            FROM tags
            WHERE tag = (SELECT x.tag
                        FROM (
                            SELECT tag, MAX(y.num)
                            FROM           
                                (SELECT tag, COUNT(tag) as num
                                FROM tags
                                GROUP BY tag) as y) as x))
        '''
common_tag = pd.read_sql(query3, con=db)
common_tag.to_csv('common_tag.csv')


import sqlite3

conn = sqlite3.connect("data.db")

c = conn.cursor()

q = "drop table if exists posts"
c.execute(q)
q = "drop table if exists foundPosts"
c.execute(q)
q = "drop table if exists comments"
c.execute(q)

q = "create table posts(id integer, name text, uid text, content text, profile text, picture text, time text, tagsChosen text)"
c.execute(q)

q = "create table foundPosts(id integer, name text, uid text, content text, profile text, picture text, time text, tagsChosen text)"
c.execute(q)

q = "create table comments(id integer, pid integer, uid text, content text, profile text, picture text, time text, lostFound text)"
c.execute(q)

conn.commit()


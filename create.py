import sqlite3

conn = sqlite3.connect("data.db")

c = conn.cursor()
'''
q = "drop table users"
c.execute(q)
q = "drop table posts"
c.execute(q)
q = "drop table comments"
c.execute(q)
'''

q = "create table users(id integer, facebookid text)"
c.execute(q)

q = "create table posts(id integer, uid integer, content text, picture text)"
c.execute(q)

q = "create table comments(id integer, pid integer, uid integer, content text)"
c.execute(q)

#q = "create table relations(uid integer, pid integer, cid integer)"
#c.execute(q)

conn.commit()


import sqlite3,hashlib, time, datetime
import json, os

path = 'data.db'

#----------------------------------Writing--------------------------------

def writePost(name,idu, newPost, profile, pic, lostFound, tags):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    if lostFound == 'lost':
        q = "SELECT MAX(id) FROM posts"
    else:
        q = "SELECT MAX(id) FROM foundPosts"
    idp = cur.execute(q).fetchone()[0]
    if idp == None:
        idp = 0
    idp += 1
    t = time.strftime('%l:%M%p, %b %d %Y')
    if tags == None:
        tags = "#"
    if lostFound == "lost":
        q = "INSERT INTO posts(id, name, uid, content, profile, picture, time, tagsChosen) VALUES(?,?,?,?,?,?,?,?)"
    elif lostFound == "found":
        q = "INSERT INTO foundPosts(id, name, uid, content, profile, picture, time, tagsChosen) VALUES(?,?,?,?,?,?,?,?)"
    cur.execute(q,(idp,name, idu, newPost, profile, pic, t, tags))
    conn.commit()
    return str(idp)

def writeComment(idp,name,idu,txt,profile,picture,lostFound):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    q = "SELECT MAX(id) FROM comments"
    idc = cur.execute(q).fetchone()[0]
    if idc == None:
        idc = 0
    print idc+1
    t = time.strftime('%l:%M%p, %b %d %Y')
    q = "INSERT INTO comments(id,pid,uid,content,profile,picture,time,lostFound) VALUES(?,?,?,?,?,?,?,?)"
    cur.execute(q,(idc+1,idp,idu,txt,profile,picture,t,lostFound))
    conn.commit()
    
#----------------------------------Deleting-------------------------------
def deleteComment(idc):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    deleteCommentH(idc)
    q = "UPDATE comments SET cid = cid-1 WHERE cid > (?)"
    cur.execute(q,(idc,))    
    conn.commit()

def deleteCommentH(idc):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    q = "DELETE FROM comments WHERE comments.cid = (?)"
    cur.execute(q,(idc,))
    conn.commit()

def deletePost(idp):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    q = "SELECT comments.cid FROM comments WHERE comments.pid = %d"
    bad = cur.execute(q%idp).fetchall()
    for comment in bad:
        deleteCommentH(comment[0])
    q = "UPDATE comments SET cid = rowid"
    cur.execute(q)
    q = "DELETE FROM posts WHERE posts.pid = %d"
    cur.execute(q%idp)
    q = "UPDATE posts SET pid = pid-1 WHERE pid > %d"
    cur.execute(q%idp)    
    conn.commit()

#writeComment("comment 1",5,9)
#writeComment("comment 2",4,9)
#deletePost(9)
#deleteComment(7)

#----------------------------------Getting--------------------------------

def getCommentsOnPost(idp, lostFound):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    if lostFound == 'lost':
        q = "SELECT * FROM comments WHERE comments.pid = ?"
    else:
        q = "SELECT * FROM comments WHERE comments.pid = ?"
    cur.execute(q,(idp,))
    all_rows = cur.fetchall()
    r = []
    for row in all_rows:
        r += [dict((cur.description[i][0], value) 
        for i, value in enumerate(row))]
    return r

def getComment(cid):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    q = "SELECT comments.* FROM comments, users WHERE comments.cid = %d AND users.id = comments.uid"
    result = cur.execute(q%cid).fetchone()
    return result

def getUserPosts(idu):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    q = "SELECT * FROM posts WHERE posts.uid = %d"
    result = cur.execute(q%idu).fetchall()
    conn.commit()
    return result

def getPost(idp,lostFound):
    schema = ('id', 'name', 'uid', 'content', 'profile', 'picture', 'time', 'tagsChosen')
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    if lostFound == 'lost':
        q = "SELECT * FROM posts WHERE posts.id = ?"
    else:
        q = "SELECT * FROM foundPosts WHERE foundPosts.id = ?"
    result = cur.execute(q,(int(idp),)).fetchone()
    conn.commit()
    a = {}
    for i,v in enumerate(result):
        a[schema[i]] = v
    return a

def getAllPosts(lostFound):
    #schema = ('id', 'name', 'uid', 'content', 'profile', 'picture', 'time', 'tagsChosen')
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    if lostFound == "lost":
        q = "SELECT * FROM posts"
    elif lostFound == "found":
        q = "SELECT * FROM foundPosts"
                
    cur.execute(q)
    all_rows = cur.fetchall()

    #Translate into JSON?
    r = []
    for row in all_rows:
        r += [dict((cur.description[i][0], value) \
              for i, value in enumerate(row))]

    #with open('params.json', 'w') as f:
    #    json.dump(r, f)

    '''
    with open('params.json', 'r') as f:
        data = json.load(f)
        print data
    '''

    final = []
    for row in all_rows:
        final.append(row)
    
    conn.commit()
    return r



def getAllUsers():
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    q = "SELECT users.name FROM users"
    cur.execute(q)
    all_rows = cur.fetchall()
    print all_rows
    conn.commit()
    return all_rows
    
def tojson(listy):
    r = []
    for row in listy:
        r += [dict((cur.description[i][0], value) 
        for i, value in enumerate(row))]
    return r

#----------------------------------Log In---------------------------------
#most of these aren't really necessary since we have facebook
    
def encrypt(word):
    hashp = hashlib.md5()
    hashp.update(word)
    return hashp.hexdigest()

def authenticate(username,password):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    q = 'SELECT users.password FROM users WHERE users.name = "%s"'
    result = cur.execute(q%username)
    for r in result:
        if(encrypt(password) == r[0]):
            return True
    conn.commit()
    return False

def getUserId(name):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    q = 'SELECT users.id FROM users WHERE users.name = "%s"'
    result = cur.execute(q%name).fetchone()
    conn.commit()
    return result[0]

def getUserName(uid):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    q = 'SELECT users.name FROM users WHERE users.id = %d'
    result = cur.execute(q%uid).fetchone()
    conn.commit()
    return result[0]

def addUser(username,password):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    q = 'SELECT users.name FROM users WHERE users.name = ?'
    result = cur.execute(q,(username,)).fetchone()
    if result == None:
        q = 'SELECT max(users.id) FROM users'
        uid = cur.execute(q).fetchone()[0]
        if uid==None:
            uid=0
        q = 'INSERT INTO users VALUES (?, ?, ?,-1,-1,"","")'
        cur.execute(q, (username, encrypt(password), uid+1))
        print str(uid+1)+","+username
        conn.commit()
        return True
    conn.commit()
    return False

'''
if __name__ == "__main__":
    writePost(1234, 'potatoes', "picture")
    print getAllPosts()
'''

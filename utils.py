import sqlite3,hashlib, time, datetime
import json

#----------------------------------Writing--------------------------------

def writePost(idu, newPost, pic):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT MAX(id) FROM posts"
    idp = cur.execute(q).fetchone()[0]
    if idp == None:
        idp = 0
    idp += 1
    print idu
    print newPost
    q = "INSERT INTO posts(id, uid, content, picture) VALUES(?,?,?,?)"
    cur.execute(q,(idp, idu, newPost, pic))
    conn.commit()
    return str(idp)

def writeComment(idp,idu,txt):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT MAX(cid) FROM comments"
    idc = cur.execute(q).fetchone()[0]
    if idc == None:
        idc = 0
    print idc+1
    q = "INSERT INTO comments(id,pid,uid,context) VALUES(?,?,?,?)"
    cur.execute(q,(idc+1,idp,idu,txt))
    conn.commit()
    
#----------------------------------Deleting-------------------------------
def deleteComment(idc):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    deleteCommentH(idc)
    q = "UPDATE comments SET cid = cid-1 WHERE cid > (?)"
    cur.execute(q,(idc,))    
    conn.commit()

def deleteCommentH(idc):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "DELETE FROM comments WHERE comments.cid = (?)"
    cur.execute(q,(idc,))
    conn.commit()

def deletePost(idp):
    conn = sqlite3.connect('data.db')
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

def getCommentsOnPost(idp):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT comments.content,datetime(comments.time,'localtime'),users.name,comments.cid,users.filename FROM comments, users WHERE comments.pid = %d AND users.id = comments.uid"
    result = cur.execute(q%idp).fetchall()
    conn.commit()
    return result

def getComment(cid):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT comments.*,users.name FROM comments, users WHERE comments.cid = %d AND users.id = comments.uid"
    result = cur.execute(q%cid).fetchone()
    return result

def getUserPosts(idu):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT * FROM posts WHERE posts.uid = %d"
    result = cur.execute(q%idu).fetchall()
    conn.commit()
    return result

def getPost(idp):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT posts.*,users.name,users.filename FROM posts,users WHERE posts.pid = %d AND posts.uid = users.id"
    result = cur.execute(q%idp).fetchone()
    conn.commit()
    return result

def getAllPosts():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    #q = "SELECT posts.content,posts.id,posts.uid,users.facebookid FROM posts, users WHERE users.id = posts.uid ORDER BY posts.id DESC"
    q = "SELECT posts.content,posts.id,posts.uid FROM posts"
    cur.execute(q)
    all_rows = cur.fetchall()

    #Translate into JSON?
    r = []
    for row in all_rows:
        r += [dict((cur.description[i][0], value) \
              for i, value in enumerate(row))]

    with open('params.json', 'w') as f:
        json.dump(r, f)

    '''
    with open('params.json', 'r') as f:
        data = json.load(f)
        print data
    '''

    final = []
    for row in all_rows:
        final.append(row)
    
    conn.commit()
    return final

getAllPosts()

def getAllUsers():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT users.name FROM users"
    cur.execute(q)
    all_rows = cur.fetchall()
    print all_rows
    conn.commit()
    return all_rows
    

#----------------------------------Log In---------------------------------
#most of these aren't really necessary since we have facebook
    
def encrypt(word):
    hashp = hashlib.md5()
    hashp.update(word)
    return hashp.hexdigest()

def authenticate(username,password):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.password FROM users WHERE users.name = "%s"'
    result = cur.execute(q%username)
    for r in result:
        if(encrypt(password) == r[0]):
            return True
    conn.commit()
    return False

def getUserId(name):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.id FROM users WHERE users.name = "%s"'
    result = cur.execute(q%name).fetchone()
    conn.commit()
    return result[0]

def getUserName(uid):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.name FROM users WHERE users.id = %d'
    result = cur.execute(q%uid).fetchone()
    conn.commit()
    return result[0]

def addUser(username,password):
    conn = sqlite3.connect('data.db')
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

from flask import Flask, render_template, session, request
from flask import redirect, url_for
import utils

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def home():
    if request.method=="GET":
        return render_template("home.html")
    else:
        newPost = request.form['newPost']
        lostFound = request.form['LostOrFound']
        tagsChosen = request.form['tagSuggest']
        prof = request.form['profile']
        pic = request.form['picture']
        name = request.form['variables']
        id = request.form['url']
        url = "<a href=/" + id + ">"
        print url
        if tagsChosen == "Select a tag below:":
            tagsChosen == None
        if lostFound == "lost":
            utils.writePost(name,id, newPost, prof, pic,"lost",tagsChosen)
            return redirect(url_for("lost"))
        elif lostFound == "found":
            utils.writePost(name,id, newPost, prof, pic,"found",tagsChosen)
            return redirect(url_for("found"))

        return redirect(url_for("lost"))

@app.route('/about', methods = ['GET','POST'])
def about():
    return render_template("about.html")

@app.route('/lost', methods = ['GET','POST'])
def lost():
    if request.method=="GET":
        lostPosts = utils.getAllPosts("lost")[::-1]
        print lostPosts
        return render_template("lost.html", lostPosts=lostPosts)

@app.route('/found', methods = ['GET','POST'])
def found():
    if request.method=="GET":
        foundPosts = utils.getAllPosts("found")[::-1]
        return render_template("found.html", foundPosts=foundPosts)
    return render_template("found.html")

@app.route('/lost/<int:post_id>', methods = ['GET','POST'])
def post(post_id):
    if request.method=="GET":
        post = utils.getPost(post_id,"lost")
        comments = utils.getCommentsOnPost(post_id)
        print 're'
        print post,comments
        return render_template("post.html",post=post, comments = comments)
    else:
        post = utils.getPost(post_id,"lost")
        comment = request.form['newComment']
        prof = request.form['profile']
        pic = request.form['picture']
        name = request.form['variables']
        id = request.form['url']
        utils.writeComment(name,post_id,comment)
        comments = utils.getCommentsOnPost(post_id,name,id,comment,prof,pic,'lost')
        return render_template("post.html", post=post, comments=comments)

@app.route('/found/<int:post_id>', methods = ['GET','POST'])
def foundPost(post_id):
    if request.method=="GET":
        post = utils.getPost(post_id,"found")
        comments = utils.getCommentsOnPost(post_id)
        print 're'
        print post,comments
        return render_template("post.html",post=post,comments=comments)
    else:
        post = utils.getPost(post_id,"found")
        comment = request.form['newComment']
        prof = request.form['profile']
        pic = request.form['picture']
        name = request.form['variables']
        id = request.form['url']
        utils.writeComment(post_id,name,id,comment,prof,pic,'found')
        comments = utils.getCommentsOnPost(post_id,'found')
        return render_template("post.html", post=post, comments=comments)
    
@app.route('/secret',methods=['POST'])
def secret():
    print request.form
    userID = request.form["variables"]
    return userID
    '''
    f = request.form
    for key in f.keys():
        for value in f.getlist(key):
            print key,":",value
    return userID
    '''

if __name__ == '__main__':
    app.secret_key = "hello"
    app.debug = True
    app.threaded = True
    app.run(host='0.0.0.0', port=8000)
else:
    app.secret_key = "hello"
    app.debug = True

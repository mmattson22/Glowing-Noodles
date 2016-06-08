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
        userID = secret()
        print userID
        if tagsChosen == "Select a tag below:":
            tagsChosen == None
        pic = "link"
        if lostFound == "lost":
            utils.writePost(userID, newPost, pic,"lost",tagsChosen)
            return redirect(url_for("lost"))
        elif lostFound == "found":
            utils.writePost(userID, newPost, pic,"found",tagsChosen)
            return redirect(url_for("found"))

        return redirect(url_for("lost"))

@app.route('/about', methods = ['GET','POST'])
def about():
    return render_template("about.html")

@app.route('/lost', methods = ['GET','POST'])
def lost():
    if request.method=="GET":
        lostPosts = utils.getAllPosts("lost")
        return render_template("lost.html", lostPosts=lostPosts)

@app.route('/found', methods = ['GET','POST'])
def found():
    if request.method=="GET":
        foundPosts = utils.getAllPosts("found")
        return render_template("found.html", foundPosts=foundPosts)
    return render_template("found.html")

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

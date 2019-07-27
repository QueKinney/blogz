from flask import Flask, request, redirect, render_template, flash, session 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'



class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String (255))
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, user):
        self.title = title
        self.body = body
        self.user = user

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blog = db.relationship('Blog', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index','blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        username = request.form["username"]
        password = request.form["password"]
        verify_password = request.form["verify_password"]
        user = User.query.filter_by(username=username).first()
   
        
        if user and user.password == password:
                session['username'] = username
                flash("Logged in")
                return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']

        error=0
        username_error=""
        password_error=""
        verify_password_error=""

        # TODO - validate user's data
        if len(username) < 3 or len(username) > 20 or not username:
            error += 1
            username_error = "Enter Valid Username"
        if len(password) < 3 or len(password) > 20 or not password:
            error += 1
            password_error = "Enter Valid Password"
        if verify_password != password:
            error += 1
            verify_password_error = "Passwords does not match"
        if error > 0:
            return render_template('signup.html', username_error=username_error, password_error=password_error, verify_password_error=verify_password_error)
        
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            flash('User Already Exist','error')
            return render_template('signup.html',username_error="User Already Exist")
    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    id = request.args.get("id")
    user = request.args.get("user")
    if id:
        id_post = Blog.query.get(id)
        return render_template('singleblog.html',blog=id_post)
    if user:
        user_post = Blog.query.filter_by(user_id=user).all()
        return render_template('blog.html', all_blog=user_post)


    else:
        all_blog = Blog.query.all()
        username = request.args.get("username")
        return render_template('blog.html',all_blog=all_blog)
    
 
#newpost should render a page where you can enter the blog
#along with displaying errors when they don't input the correct things
#make sure to call a method.request for post that way you don't run into errors

@app.route('/newpost', methods=['POST','GET'])
def newpost():
    user = User.query.filter_by(username=session['username']).first()    

    #start with this if since this will be both a GET and POST page
    if request.method == 'POST':  
        title = request.form["title"]
        body = request.form["body"]
        new_blog = Blog(title,body,user)
        db.session.add(new_blog)
        db.session.commit()
        
        return render_template ("singleblog.html",blog=new_blog)
    else:    
        return render_template('newpost.html')

@app.route("/", methods=['GET'])
def index():
    blog = User.query.join(Blog).all()
    return render_template("index.html",blogs=blog) 

 
    

#leave this as is
if __name__ == '__main__':
    app.run()
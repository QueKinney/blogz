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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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
    allowed_routes = ['login', 'signup']
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
        verify = request.form['verify_password']

        # TODO - validate user's data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            flash('User Already Exist','error')
    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    id = request.args.get("id")
    if id:
        id_post = Blog.query.get(id)
        return render_template('individual.html',all_blog=id_post)
    else:
        all_blog = Blog.query.all()
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
        blog = Blog.query.order_by('-Blog.id').first()
        return render_template ("singleblog.html",blog=blog)
    else:    
        return render_template('newpost.html')

@app.route("/", methods=['GET'])
def index():
     return render_template("base.html") 

 
    

#leave this as is
if __name__ == '__main__':
    app.run()
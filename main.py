from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:YES@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'



class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String (255))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password


#app routes for blog, newpost

#blog should render the blogs in order with a link for them to pull up individually
#individual can be posted under here in an if else statement. 
#if you're not displaying blog you will display the individual post

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
    

    #start with this if since this will be both a GET and POST page
    if request.method == 'POST':
        title_error = ""
        blog_error = ""

        title = request.form["title"]
        blog = request.form["blog"]
        error = 0

        if len(title) < 3:
            error +=1
            title_error = "Please Enter a title"
        if len(blog) < 3:
            error += 1 
            blog_error ="Enter a blog Post"
        if error !=0:
            return render_template('newpost.html',title=title,title_error=title_error,blog=blog,blog_error=blog_error)
        else:
            #rewrite this to fit into your posts to save it to the server
        #make sure to make checks to see if everything is correct before saving the server
            new_blog = Blog(title,blog)
            db.session.add(new_blog)
            db.session.commit()
            return redirect ("/blog?id=" + str(new_blog.id))
    else:  
        return render_template('newpost.html')

app.route("/", methods=['GET'])
    def index():
        return render_template("base.html") 
    @app.route("/validate", methods = ['POST'])
    def validate(): 
        error = 0
        username_error = ""
        password_error = ""
        verify_password_error = ""
        email_error = ""

        username = request.form["username"]
        password = request.form["password"]
        verify_password = request.form["verify_password"]
        email = request.form["email"]


        if len(username) < 3 or len(username) > 20:
            error += 1
            username_error = "Enter Valid Username"
        if len(password) < 3 or len(password) > 20:
            error += 1
            password_error = "Enter Valid Password"
        if verify_password != password:
            error += 1
            verify_password_error = "Passwords does not match"
        if email != "":
            
            if ("@"  not in email) or("." not in email):
                error +=1
                email_error = "Enter valid email"
        if error!= 0:
            return render_template("base.html",username=username,username_error=username_error,password_error=password_error,verify_password_error=verify_password_error, email_error=email_error)
        else:
            return render_template("hello.html",username=username,password=password,verify_password=verify_password,email=email)


#leave this as is
if __name__ == '__main__':
    app.run()
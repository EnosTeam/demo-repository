from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    birth_date = db.Column(db.String(10), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    letter = db.Column(db.Text, nullable=False)
with app.app_context():
    db.create_all()

@app.route('/')
def door():
    return render_template('KSC_Web_Main_New.html')

@app.route('/h')
def home():
    return render_template('KSC_Web_Main_New.html')

@app.route('/i')
def intro():
    return render_template('KSC_Web_introduce.html')

@app.route('/inup')
def inup():
    return render_template('KSC_Web_Sign_in.html')

@app.route('/Signup', methods = ['Get', 'Post'])
def Signup():
    if request.method == 'POST':
        # Get form data from the request
        username = request.form.get('ID')
        password = request.form.get('PW')
        email = request.form.get('Mail')
        birth_date = request.form.get('BR')
        first_name = request.form.get('FN')
        last_name = request.form.get('LN')

        # Create a new User object
        new_user = User(
            username=username,
            password=password,  # You should hash the password for security purposes
            email=email,
            birth_date=birth_date,
            first_name=first_name,
            last_name=last_name
        )
        
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('Signup'))
    return render_template('KSC_Web_Sign_up.html')

@app.route('/noti')
def noti():
    return render_template('KSC_Web_Notice.html')

@app.route('/p')
def index():
    posts = Post.query.all()
    return render_template('KSC_Web_Post.html', posts=posts)

@app.route('/post', methods=['POST'])
def post():
    title = request.form.get('title')
    letter = request.form.get('letter')
    new_post = Post(title=title, letter=letter)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/post/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.letter = request.form['letter']
        db.session.commit()
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('edit_post.html', post=post)

@app.route('/search', methods=['GET'])
def search_post():
    keyword = request.args.get('keyword', '')
    if keyword:
        posts = Post.query.filter(or_(Post.title.contains(keyword), Post.letter.contains(keyword))).all()
    else:
        posts = Post.query.all() 
    return render_template('KSC_Web_Post_Search.html', posts=posts, keyword=keyword)

if __name__ == '__main__':
    app.run(debug=True)
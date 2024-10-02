from flask import Flask, request, render_template, redirect, url_for,flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

db = SQLAlchemy(app)
#set secret key
app.secret_key = 'secret_key'
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
    print(session)
    return render_template('KSC_Web_Main_New.html')

@app.route('/i')
def intro():
    return render_template('KSC_Web_introduce.html')

@app.route('/inup', methods=['GET', 'POST'])
def inup():
    if request.method == 'POST':
        # Get form data from the login form
        username = request.form.get('ID')
        password = request.form.get('PW')

        # Find user in the database
        user = User.query.filter_by(username=username).first()

        # Check if user exists and password is correct (you should use password hashing in production)
        if user and user.password == password:
            session['user_id'] = user.id
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            
            return redirect(url_for('home'))
        else:
            # Invalid credentials, show error
            flash('Invalid username or password. Please try again.', 'danger')
            return redirect(url_for('inup'))

    # If it's a GET request or login failed, render the login page
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

         # Check if the username or email already exists in the database
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            flash('Username or Email already exists. Please choose a different one.', 'danger')
            return redirect(url_for('inup'))  # Redirect back to signup form

        # Create a new User object if the username/email is not taken
        new_user = User(
            username=username,
            password=password,  # Remember to hash the password for security
            email=email,
            birth_date=birth_date,
            first_name=first_name,
            last_name=last_name
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful!')
        return redirect(url_for('home'))  # Redirect to the home page
    return render_template('KSC_Web_Sign_up.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Clear the login session
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('home'))  # Redirect to home page

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
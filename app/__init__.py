from flask import Flask, url_for, render_template, request, redirect, session,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory, flash
#from flask_file_upload import FileUpload

UPLOAD_FOLDER = '/home/kinshuk/Projects/Crypto-project/Crypto_project/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.secret_key = "ThisIsNotASecret:p"


db = SQLAlchemy(app)
#file_upload = FileUpload(app,db)
#db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    #file = file_upload.Column()

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('index.html', message="Hello!")


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(username=request.form['username'], password=request.form['password']))
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('index.html', message="User Already Exists")
    else:
        return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['username']
        p = request.form['password']
        #session['username'] = u
        #session['password'] = p
        data = User.query.filter_by(username=u, password=p).first()
        if data is not None:
            session['logged_in'] = True

            return redirect(url_for('index'))
        return render_template('index.html', message="Incorrect Details")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/inbox', methods = ['GET','POST'])
def inbox():

    return render_template('inbox.html')
@app.route('/send', methods = ['GET','POST'])
def send():

    return render_template('send.html')
    
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #User_post = User(user_username,user_password)
            #file_upload.save_files(User_post,files = {'file':file})
            #return redirect(url_for('uploaded_file',filename=filename))
            flash("file uploaded successfully",'Success')
        else: 
            flash('Upload Failed. Try again','Error:') 
            return render_template('upload.html',message= "File uploaded")

    return render_template('upload.html',message= "Upload Failed")

from werkzeug.middleware.shared_data import SharedDataMiddleware
app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))
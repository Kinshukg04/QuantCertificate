from app import app, db
from app.models.models import User, Message
from app.src import qcalgos
from flask import url_for, render_template, request, redirect, flash, send_from_directory, session
from werkzeug.utils import secure_filename
import os
from PIL import Image

# Allowed files
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('index.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if session.get('logged_in'):
        return render_template('home.html')

    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        try:
            # Add the user to db
            # TODO: Encrypt the password
            db.session.add(User(username=request.form['username'], password=request.form['password']))
            db.session.commit()

            return redirect(url_for('login'))
        except:
            return render_template('index.html', message="User Already Exists")

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()

        if data is not None:
            # Log in
            session['logged_in'] = True
            session['user_id']  = data.user_id
            session['username'] = data.username

            return redirect(url_for('index'))

        return render_template('index.html', message="Incorrect details or User does not exist!!")

@app.route('/inbox', methods = ['GET'])
def inbox():
    return render_template('inbox.html')

@app.route('/send', methods = ['GET','POST'])
def send():
    return render_template('send.html')
    
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            flash("file uploaded successfully",'Success')
        else: 
            flash('Upload Failed. Try again','Error:') 
            return render_template('upload.html',message= "Upload Failed")
        
        recipeint_username = request.form['recipeint_username']
        subject = request.form['subject']
        if User.query.filter_by(username=recipeint_username).first() is None:
            return render_template('upload.html',message= "Upload Failed")

        # Perform crypto
        hashed_data = qcalgos.hash_image(Image.open(filepath))
        key = qcalgos.create_quantum_shared_key(max_size=256)
        nonce, ciphertext, tag = qcalgos.encrypt(key, hashed_data, key_size=256)
        
        # Add to the database
        db.session.add(Message(
            sent_by=session['user_id'],
            received_by=User.query.filter_by(username=recipeint_username).first().user_id,
            title=subject,
            filepath=filepath,
            hashed_data=hashed_data,
            nonce=nonce,
            ciphertext=ciphertext,
            tag=tag,
            key=key
        ))
        db.session.commit()

    return render_template('upload.html')

# from werkzeug.middleware.shared_data import SharedDataMiddleware
# app.add_url_rule('/uploads/<filename>', 'uploaded_file',
#                  build_only=True)
# app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
#     '/uploads':  app.config['UPLOAD_FOLDER']
# })
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))
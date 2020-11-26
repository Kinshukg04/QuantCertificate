from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    #file = file_upload.Column()s

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Message(db.Model):
    messsage_id = db.Column(db.Integer, primary_key=True)
    sent_by = db.Column(db.Integer)
    received_by = db.Column(db.Integer)
    title = db.Column(db.String(300))
    filepath = db.Column(db.String(300))
    hashed_data = db.Column(db.String(1024))

    def __init__(self, sent_by, received_by, title, filepath, hashed_data, nonce, ciphertext, tag, key):
        self.sent_by = sent_by
        self.received_by = received_by
        self.title = title
        self.filepath = filepath
        self.hashed_data = hashed_data
        self.nonce = nonce
        self.ciphertext = ciphertext
        self.tag = tag
        self.key = key

# class Room(db.Model):
#     room_id = db.Column(db.Integer, primary_key=True)

#     def __init__(self, usera, userb, shared_key, nonce, ciphertext, tag):
#         pass
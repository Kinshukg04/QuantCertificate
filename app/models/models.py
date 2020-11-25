from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    #file = file_upload.Column()s

    def __init__(self, username, password):
        self.username = username
        self.password = password


# class File(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     file_path = db.Column(db.String(200))
#     file_title = db.Column(db.String(20))

#     def __init__(self,id,file_path,file_title):
#         self.id = id
#         self.file_path = file_path
#         self.file_title = file_title

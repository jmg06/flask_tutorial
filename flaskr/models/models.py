from flask_sqlalchemy import SQLAlchemy

# Database instance
db = SQLAlchemy()

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    minutes = db.Column(db.Integer)
    seconds = db.Column(db.Integer)
    songwriter = db.Column(db.String(128))
    
    def __repr__(self):
        return f'{self.title} - {self.minutes} - {self.seconds} - {self.songwriter}'

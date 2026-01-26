# By default, Flask search for this file to use it as the entry point.
# If want to use a different file name, must have to change a ENV and specify the new name.

from flaskr import create_app

from .models import db, Song

# Create app context
app = create_app('default')
app_context = app.app_context()
app_context.push()

# Initialize flask app
db.init_app(app)
db.create_all()

with app.app_context():
    song = Song(title='Test', minutes=2, seconds=30, songwriter='Juan')
    db.session.add(song)
    db.session.commit()
    print(Song.query.all())

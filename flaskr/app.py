# By default, Flask search for this file to use it as the entry point.
# If want to use a different file name, must have to change a ENV and specify the new name.

from flaskr import create_app

from .models import Album, Format, Song, User, db

# Create app context
app = create_app("default")
app_context = app.app_context()
app_context.push()

# Initialize flask app
db.init_app(app)
db.create_all()

with app.app_context():
    user = User(name="Juan", password="123456")

    album = Album(
        title="Test",
        year=1999,
        description="Voluptate quis ut aute.",
        format=Format.CASSETTE,
    )

    user.albums.append(album)

    song = Song(title="Test", minutes=2, seconds=30, performer="Juan")

    album.songs.append(song)

    db.session.add(user)
    db.session.add(song)
    db.session.commit()

    print(Album.query.all())
    print(Album.query.all()[0].songs)
    print(Song.query.all())

    db.session.delete(user)
    db.session.commit()

    print(Album.query.all())
    print(Song.query.all())

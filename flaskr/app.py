# By default, Flask search for this file to use it as the entry point.
# If want to use a different file name, must have to change a ENV and specify the new name.

from flaskr import create_app

from .models import Album, AlbumShcema, Format, Song, User, db

# Create app context
app = create_app("default")
app_context = app.app_context()
app_context.push()

# Initialize flask app
db.init_app(app)
db.create_all()

with app.app_context():
    album_schema = AlbumShcema()

    album = Album(
        title="Test",
        year=1999,
        description="Voluptate quis ut aute.",
        format=Format.CASSETTE,
    )

    db.session.add(album)
    db.session.commit()

    print([album_schema.dumps(album) for album in Album.query.all()])

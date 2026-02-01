import enum

from flask_sqlalchemy import SQLAlchemy

# Database instance
db = SQLAlchemy()

album_song = db.Table(
    "album_song",
    db.Column("album_id", db.Integer, db.ForeignKey("album.id"), primary_key=True),
    db.Column("song_id", db.Integer, db.ForeignKey("song.id"), primary_key=True),
)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    minutes = db.Column(db.Integer)
    seconds = db.Column(db.Integer)
    performer = db.Column(db.String(128))
    albums = db.relationship("Album", secondary="album_song", back_populates="songs")

    def __repr__(self):
        return f"{self.title} - {self.minutes} - {self.seconds} - {self.performer}"


class Format(enum.Enum):
    DISC = 1
    CASSETTE = 2
    CD = 3


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    year = db.Column(db.Integer)
    description = db.Column(db.String(256))
    format = db.Column(db.Enum(Format))
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    # back_populates tells to update the albums if there is a change in a album_song
    songs = db.relationship("Song", secondary="album_song", back_populates="albums")
    __table_args__ = (
        db.UniqueConstraint("user", "title", name="unique_album_title"),
    )  # Constraint: 1 user can't have albums with the same name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(32))
    albums = db.relationship("Album", cascade="all, delete, delete-orphan")

from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from ..models import Album, AlbumShcema, Song, SongSchema, User, UserSchema, db

# ? Resources provides necessary resources for implementing CRUD operations, consumed via HTTP

# * Song Operations
song_schema = SongSchema()
user_schema = UserSchema()
album_schema = AlbumShcema()


class SongsView(Resource):
    def get(self):
        return [song_schema.dump(song) for song in Song.query.all()]

    def post(self):
        new_song = Song(
            title=request.json["title"],
            minutes=request.json["minutes"],
            seconds=request.json["seconds"],
            performer=request.json["performer"],
        )

        db.session.add(new_song)
        db.session.commit()

        return song_schema.dump(new_song)


class SongView(Resource):
    def get(self, song_id):
        return song_schema.dump(Song.query.get_or_404(song_id))

    def put(self, song_id):
        db_song = Song.query.get_or_404(song_id)

        db_song.title = request.json.get("title", db_song.title)
        db_song.minutes = request.json.get("minutes", db_song.minutes)
        db_song.seconds = request.json.get("seconds", db_song.seconds)
        db_song.performer = request.json.get("performer", db_song.performer)

        db.session.commit()

        return song_schema.dump(db_song)

    def delete(self, song_id):
        db_song = Song.query.get_or_404(song_id)

        db.session.delete(db_song)

        db.session.commit()

        return "Song successfully deleted.", 204


# * User Operations
class LogInView(Resource):
    def post(self):
        db_usuario = User.query.filter(
            User.name == request.json["name"], User.password == request.json["password"]
        ).first()

        if db_usuario is None:
            return {"message": "Invalid credentials."}, 401
        else:
            access_token = create_access_token(identity=db_usuario.id)
            return {
                "status_code": 200,
                "message": "User successfully logged in.",
                "access_token": access_token,
            }


class SignInView(Resource):
    def post(self):
        new_user = User(name=request.json["name"], password=request.json["password"])
        access_token = create_access_token(identity=request.json["name"])
        db.session.add(new_user)
        db.session.commit()
        return {
            "status_code": 201,
            "message": "User successfully created.",
            "access_token": access_token,
        }

    def put(self, user_id):
        db_user = User.query.get_or_404(user_id)
        db_user.name = request.json.get("name", db_user.name)
        db_user.password = request.json.get("password", db_user.password)
        db.session.commit()
        return user_schema.dump(db_user)

    def delete(self, user_id):
        db_user = User.query.get_or_404(user_id)
        db.session.delete(db_user)
        db.session.commit()
        return "User successfully deleted.", 204


class UserAlbumView(Resource):
    @jwt_required()
    def post(self, user_id):
        new_album = Album(
            title=request.json["title"],
            year=request.json["year"],
            description=request.json["description"],
            format=request.json["format"],
        )
        db_user = User.query.get_or_404(user_id)
        db_user.albums.append(new_album)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "The user already has an album with that name.", 409

        return album_schema.dump(new_album)

    @jwt_required()
    def get(self, user_id):
        db_user = User.query.get_or_404(user_id)
        return [album_schema.dump(album) for album in db_user.albums]


# * Album Operations
class AlbumSongView(Resource):
    def post(self, album_id):
        db_album = Album.query.get_or_404(album_id)

        if "song_id" in request.json.keys():
            db_song = Song.query.get(request.json["song_id"])
            if db_song is not None:
                db_album.songs.append(db_song)
                db.session.commit()
            else:
                return f"Song with id {request.json['song_id']} not found.", 404
        else:
            new_song = Song(
                title=request.json["title"],
                minutes=request.json["minutes"],
                seconds=request.json["seconds"],
                performer=request.json["performer"],
            )
            db_album.songs.append(new_song)
        db.session.commit()
        return album_schema.dump(db_album)

    def get(self, album_id):
        db_album = Album.query.get_or_404(album_id)
        return [song_schema.dump(song) for song in db_album.songs]


class AlbumView(Resource):
    def get(self, album_id):
        return album_schema.dump(Album.query.get_or_404(album_id))

    def put(self, album_id):
        db_album = Album.query.get_or_404(album_id)
        db_album.title = request.json.get("title", db_album.title)
        db_album.year = request.json.get("year", db_album.year)
        db_album.description = request.json.get("description", db_album.description)
        db_album.format = request.json.get("format", db_album.format)
        db.session.commit()
        return album_schema.dump(db_album)

    def delete(self, album_id):
        db_album = Album.query.get_or_404(album_id)
        db.session.delete(db_album)
        db.session.commit()
        return "Album successfully deleted.", 204

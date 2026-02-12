# By default, Flask search for this file to use it as the entry point.
# If want to use a different file name, must have to change a ENV and specify the new name.

from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from flaskr import create_app

from .models import db
from .views import (
    AlbumSongView,
    AlbumView,
    LogInView,
    SignInView,
    SongsView,
    SongView,
    UserAlbumView,
)

# Create app context
app = create_app("default")
app_context = app.app_context()
app_context.push()

# Initialize flask app
db.init_app(app)
db.create_all()

# CORS Config
cors = CORS(app)

# Initialize Restful API
api = Api(app)

api.add_resource(SongsView, "/songs")
api.add_resource(SongView, "/song/<int:song_id>")
api.add_resource(SignInView, "/signin")
api.add_resource(LogInView, "/login")
api.add_resource(UserAlbumView, "/user/<int:user_id>/albums")
api.add_resource(AlbumView, "/album/<int:album_id>")
api.add_resource(AlbumSongView, "/album/<int:album_id>/songs")

jwt = JWTManager(app)

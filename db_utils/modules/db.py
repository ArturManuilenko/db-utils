from typing import NamedTuple

import flask_sqlalchemy
from flask import Flask

db = flask_sqlalchemy.SQLAlchemy()


class DbConfig(NamedTuple):
    uri: str
    track_mod: bool = False


def attach_to_flask_app(app: Flask, config: DbConfig) -> Flask:
    app.config['SQLALCHEMY_DATABASE_URI'] = config.uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.track_mod
    # TODO: add some config options
    db.init_app(app)
    return app

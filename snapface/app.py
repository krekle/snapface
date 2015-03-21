# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from flask import Flask, render_template
from flask.ext.admin.contrib.sqla import ModelView
import inspect
import os
import sys
from snapface import public
from snapface import user
from snapface.settings import ProdConfig
from snapface.assets import assets
from snapface.extensions import (
    bcrypt,
    cache,
    db,
    login_manager,
    migrate,
    debug_toolbar,
    admin,
)

def create_app(config_object=ProdConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    python_path()
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    initialize_admin()
    return None


def initialize_admin():
    from snapface.user.models import User
    admin.add_view(ModelView(User, db.session, endpoint="users"))
    from snapface.bots.models import Bot
    admin.add_view(ModelView(Bot, db.session))
    from snapface.bots.models import Friend
    admin.add_view(ModelView(Friend, db.session))
    return None


def register_blueprints(app):
    app.register_blueprint(public.views.public_controller)
    app.register_blueprint(user.views.user_controller)
    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None

# Adding the whole working tree to the pythonpath, to avoid import errors
def python_path():
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)

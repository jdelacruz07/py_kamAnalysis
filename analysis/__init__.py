import os

from flask import Flask
from . import db
from . import auth
from . import gap
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True, static_folder='static/app', static_url_path="/app")
    CORS(app, supports_credentials=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'analysis.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def index(path):
        print(path)
        return app.send_static_file("index.html")

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(gap.bp)
    # app.add_url_rule('/', endpoint='index')
    return app


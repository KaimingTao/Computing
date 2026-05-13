from pathlib import Path

from flask import Flask


# Factory
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        Path(app.instance_path).mkdir()
    except FileExistsError:
        pass

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=str(Path(app.instance_path) / 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)


    from . import db    
    db.init_app(app)


    from . import auth
    app.register_blueprint(auth.bp)


    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')



    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
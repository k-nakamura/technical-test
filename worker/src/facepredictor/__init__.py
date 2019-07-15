from flask import Flask, render_template


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    from .api import api
    app.register_blueprint(api, url_prefix='/api')

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('index.html')

    return app

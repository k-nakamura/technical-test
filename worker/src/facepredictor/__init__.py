from flask import Flask, render_template, current_app


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    from .api import api
    app.register_blueprint(api, url_prefix='/api')

    @app.route('/', methods=['GET', 'POST'])
    def index():
        arrowed_ext = current_app.config['ARROWED_EXT']
        return render_template('index.html', arrowed_ext=arrowed_ext)

    return app

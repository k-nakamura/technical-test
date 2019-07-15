from . import facepredictor
from . import config

app = facepredictor.create_app(config)


if __name__ == "__main__":
    app.run()

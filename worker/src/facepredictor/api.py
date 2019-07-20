from flask import request, jsonify, current_app, Blueprint
from werkzeug import secure_filename
from . import model
import tempfile
from os import path

api = Blueprint('api', __name__)


@api.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.files.get('image') is None or \
            request.files.get('image').filename == '':
        return jsonify({'err_message': 'ファイルが選択されていません。'})

    img_file = request.files['image']
    img_name = secure_filename(img_file.filename)
    tmp_dir = tempfile.TemporaryDirectory()
    img_file.save(path.join(tmp_dir.name, img_name))
    image_path = tmp_dir.name + "/" + img_name

    _, ext = path.splitext(image_path)
    if ext not in current_app.config['ARROWED_EXT']:
        return jsonify({'err_message': 'この拡張子のファイルは処理できません。'})

    result = model.predict(image_path)

    return jsonify(result)

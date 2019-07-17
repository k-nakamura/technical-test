from flask import request, jsonify, Blueprint
from werkzeug import secure_filename
from . import model
import tempfile
import os

api = Blueprint('api', __name__)


@api.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.files.get('image') is None:
        return jsonify({'message': 'Image is not uploaded.'})
    img_file = request.files['image']
    img_name = secure_filename(img_file.filename)
    tmp_dir = tempfile.TemporaryDirectory()
    img_file.save(os.path.join(tmp_dir.name, img_name))

    print('tmp_dir.name', tmp_dir.name)
    print('img_name', img_name)
    print(tmp_dir.name + '/' + img_name)

    result = model.predict(tmp_dir.name)

    return jsonify(result)

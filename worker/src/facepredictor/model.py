from flask import current_app
import cv2
import dlib
import numpy as np
from .submodule.pre_trained_model.wide_resnet import WideResNet
from base64 import b64encode
from os import path


def predict(image_path):
    depth = current_app.config['DEPTH']
    k = current_app.config['WIDTH']
    weight_file = current_app.config['WEIGHT_FILE']
    margin = current_app.config['MARGIN']

    result = dict()
    result['labels'] = dict()
    result['image'] = None

    # 顔を検出するためのモデル
    detector = dlib.get_frontal_face_detector()

    # 性別、年齢を予測するモデル
    img_size = 64
    model = WideResNet(img_size, depth=depth, k=k)()
    model.load_weights(weight_file)

    # 画像読み込み
    img = read_image(image_path)
    input_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_h, img_w, _ = np.shape(input_img)

    # 顔を検出する
    detected = detector(input_img, 1)
    faces = np.empty((len(detected), img_size, img_size, 3))

    if len(detected) > 0:
        # 検出した顔を切り出す
        for i, d in enumerate(detected):
            x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, \
                d.bottom() + 1, d.width(), d.height()
            xw1 = max(int(x1 - margin * w), 0)
            yw1 = max(int(y1 - margin * h), 0)
            xw2 = min(int(x2 + margin * w), img_w - 1)
            yw2 = min(int(y2 + margin * h), img_h - 1)
            # 検知した顔を長方形で囲う
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            faces[i, :, :, :] \
                = cv2.resize(img[yw1:yw2 + 1, xw1:xw2 + 1, :], (img_size, img_size))

        # 切り出した顔画像の性別と年齢を予測する
        results = model.predict(faces)
        predicted_genders = results[0]
        ages = np.arange(0, 101).reshape(101, 1)
        predicted_ages = results[1].dot(ages).flatten()

        for i, d in enumerate(detected):
            # レスポンスとして返すラベル情報
            label = dict()
            label['gender'] = "M" if predicted_genders[i][0] < 0.5 else "F"
            label['age'] = int(predicted_ages[i])
            result['labels'][i] = label

            # 予測結果を画像に追記
            text = "({}){}, {}".format(i, label['age'], label['gender'])
            draw_label(img, (d.left(), d.top()), text)

    result['image'] = get_base64_image(image_path, img)

    return result


def read_image(image_path):
    img = cv2.imread(str(image_path), 1)

    if img is not None:
        h, w, _ = img.shape
        r = 640 / max(w, h)
        return cv2.resize(img, (int(w * r), int(h * r)))

    return None


def draw_label(image, point, label, font=cv2.FONT_HERSHEY_SIMPLEX,
               font_scale=0.8, thickness=1):
    size = cv2.getTextSize(label, font, font_scale, thickness)[0]
    x, y = point
    cv2.rectangle(image, (x, y - size[1]), (x + size[0], y), (255, 0, 0), cv2.FILLED)
    cv2.putText(image, label, point, font, font_scale, (255, 255, 255), thickness, lineType=cv2.LINE_AA)


def get_base64_image(image_path, img):
    cv2.imwrite(image_path, img)
    with open(image_path, 'rb') as f:
        result_img = f.read()
    encoded_image = ''

    _, ext = path.splitext(image_path)
    if ext in ['.jpeg', '.jpg', '.jpe']:
        encoded_image = 'data:image/jpeg;base64,' + \
            b64encode(result_img).decode("utf-8")
    elif ext in ['.png']:
        encoded_image = 'data:image/png;base64,' + \
            b64encode(result_img).decode("utf-8")

    return encoded_image

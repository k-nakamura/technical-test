FROM gcr.io/google-appengine/python

# Python3.6の仮想環境
RUN virtualenv -p python3.6 /env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# OpenCVのエラー対策
RUN apt-get update
RUN apt-get install -y libsm6 libxext6 libxrender-dev

# 必要なライブラリをpipでinstall
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# CMakeを必要とするためdlibだけは分けてinstall
RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

# ソースコードを配置してsrcに移動
RUN mkdir /var/www
COPY src /var/www/src
WORKDIR /var/www/src

# uwsig用のユーザーを作成して権限を付与
RUN useradd -m uwsgi_user
RUN chown -R uwsgi_user:uwsgi_user /var/www/src/

# uwsgiを実行
CMD ["uwsgi","--ini","/var/www/src/uwsgi.ini","--uid","uwsgi_user"]

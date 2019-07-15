FROM gcr.io/google-appengine/python

RUN virtualenv -p python3.6 /env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# OpenCVのエラー対策
RUN apt-get update
RUN apt-get install -y libsm6 libxext6 libxrender-dev

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# CMakeを必要とするためdlibだけは分けてinstall
RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

RUN mkdir /var/www
WORKDIR /var/www
COPY src /var/www/src

# uwsgi.iniをコピー
ADD uwsgi.ini /var/www/uwsgi.ini
CMD ["uwsgi","--ini","/var/www/uwsgi.ini"]

FROM gcr.io/google-appengine/python

RUN mkdir /var/www
WORKDIR /var/www
ADD src /var/www/src

RUN virtualenv -p python3.6 /env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# uwsgi.iniをコピー
COPY uwsgi.ini /var/www/uwsgi.ini
CMD ["uwsgi","--ini","/var/www/uwsgi.ini"]

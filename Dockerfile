FROM python

ADD requirements.txt /app/requirements.txt

WORKDIR /app
RUN set -ex \
    && python3 -m venv /env \
    && /env/bin/pip3 install --upgrade pip \
    && /env/bin/pip3 install -r requirements.txt

ADD . /app

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000

CMD ["/app/runserver.sh"]
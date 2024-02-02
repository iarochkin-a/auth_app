FROM python:3.12

RUN mkdir auth_app

ADD requirements.txt /auth_app

WORKDIR /auth_app

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm requirements.txt

ADD . /auth_app

CMD ["/bin/bash", "start.sh"]

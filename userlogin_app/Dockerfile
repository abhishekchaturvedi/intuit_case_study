FROM python:3.7.4-slim-buster

ENV INSTALL_PATH /userlogin_app
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD gunicorn -b 0.0.0.0:8001 --access-logfile - "userlogin.app:create_app()"

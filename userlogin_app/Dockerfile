FROM python:3.7.4-slim-buster

ENV INSTALL_PATH /userlogin_app
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
## Will install everything from requirements.txt
RUN pip install -r requirements.txt
COPY . .

## Will run setup.py to install the CLI.
RUN pip install --editable .

CMD gunicorn -b 0.0.0.0:8001 --access-logfile - --error-logfile - --reload "userlogin.app:create_app()"

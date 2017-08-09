FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y build-essential git python3 python3-pip curl

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash
RUN apt-get install -y nodejs

RUN pip3 install --upgrade pip

RUN apt-get install -y libffi-dev
RUN apt-get install -y libssl-dev g++ gcc
RUN apt-get install -y libmysqlclient-dev

RUN apt-get install -y nginx gunicorn supervisor
RUN apt-get install -y uwsgi

RUN apt-get install -y bcrypt

RUN pip install uwsgi

RUN npm install -g chartist

ADD requirements.txt /sherlock/
RUN pip3 install -r /sherlock/requirements.txt

ADD frontsherlock/package.json /sherlock/frontsherlock/
WORKDIR /sherlock/frontsherlock/
RUN npm install --no-optional
COPY . /sherlock
RUN npm run build
WORKDIR /sherlock/
# Temporary Item (we gonna move to mysql)
RUN rm -rf sherlockapi/data/sherlock.db
RUN python3 setup_container.py

RUN rm /etc/nginx/sites-enabled/default
COPY app_nginx.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/app_nginx.conf /etc/nginx/sites-enabled/app_nginx.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Setup Supervisor
RUN mkdir -p /var/log/supervisor/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8080
EXPOSE 80
EXPOSE 443
EXPOSE 4567

CMD ["supervisord", "-n"]

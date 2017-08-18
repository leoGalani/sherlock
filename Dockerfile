FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y build-essential git python3 python3-pip curl

RUN pip3 install --upgrade pip

RUN apt-get install -y libffi-dev
RUN apt-get install -y libssl-dev g++ gcc
RUN apt-get install -y libmysqlclient-dev
RUN apt-get install -y libyaml-dev
RUN apt-get install -y nginx gunicorn supervisor
RUN apt-get install -y bcrypt

ADD requirements.txt /sherlock/
RUN pip3 install -r /sherlock/requirements.txt

COPY . /sherlock

WORKDIR /sherlock/frontsherlock/

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash && \
    apt-get install -y nodejs && \
    npm install && \
    npm run build && \
    rm -rf /sherlock/frontsherlock/node_modules && \
    apt-get remove -y nodejs && \
    apt-get autoremove -y

WORKDIR /sherlock/

RUN rm /etc/nginx/sites-enabled/default
COPY app_nginx.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/app_nginx.conf /etc/nginx/sites-enabled/app_nginx.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Setup Supervisor
RUN mkdir -p /var/log/supervisor/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80

CMD ["supervisord", "-n"]

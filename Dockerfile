FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive

ADD requirements.txt /sherlock/

RUN apt-get update && \
    apt-get install -y libffi-dev bcrypt build-essential && \
    apt-get install -y git python3 python3-pip && \
    apt-get install -y libmysqlclient-dev libyaml-dev nginx gunicorn supervisor && \
    python3 -m pip install --user --upgrade pip==9.0.3 && \
    pip3 install -r /sherlock/requirements.txt && \
    apt-get remove -y libffi-dev bcrypt build-essential && \
    apt-get autoremove -y && \
    apt-get clean

COPY . /sherlock
WORKDIR /sherlock/frontsherlock/

RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -sL https://deb.nodesource.com/setup_8.x | bash && \
    apt-get install -y nodejs bzip2 && \
    npm install && \
    npm run build && \
    rm -rf /sherlock/frontsherlock/node_modules && \
    apt-get remove -y gnupg nodejs curl && \
    apt-get autoremove -y && \
    apt-get clean

WORKDIR /sherlock/

RUN rm /etc/nginx/sites-enabled/default
COPY app_nginx.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/app_nginx.conf /etc/nginx/sites-enabled/app_nginx.conf && \
    echo "daemon off;" >> /etc/nginx/nginx.conf

# Setup Supervisor
RUN mkdir -p /var/log/supervisor/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80

CMD ["supervisord", "-n"]

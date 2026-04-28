FROM alpine:3.19.1

ENV PYTHONUNBUFFERED 1
RUN apk add --no-cache bash build-base curl git nodejs npm postgresql-dev py3-pip python3 python3-dev supervisor

RUN mkdir -p /opt/webtetrado
WORKDIR /opt/webtetrado/

COPY requirements.txt /opt/webtetrado/requirements.txt
RUN pip3 install --break-system-packages -r requirements.txt \
 && pip3 install --break-system-packages git+https://github.com/celery/django-celery-beat#egg=django-celery-beat

WORKDIR /opt/webtetrado/frontend
COPY frontend/package.json /opt/webtetrado/frontend/package.json
RUN npm install

WORKDIR /opt/webtetrado/
COPY . /opt/webtetrado/

RUN chmod a+x frontend/compile_less.sh
RUN cd /opt/webtetrado/frontend \
 && npm run build --scripts-prepend-node-path=auto \
 && find dist -name "*.map" -delete

COPY build/celery_worker_docker.conf /etc/supervisor/conf.d/
COPY build/celery_beat_docker.conf /etc/supervisor/conf.d/
COPY build/worker_supervisor.conf /etc/supervisor/conf.d/
COPY build/ws_supervisor.conf /etc/supervisor/conf.d/
COPY build/web_supervisor.conf /etc/supervisor/conf.d/
RUN echo "files = /etc/supervisor/conf.d/*.conf" >> /etc/supervisord.conf
WORKDIR /opt/webtetrado

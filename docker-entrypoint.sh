#!/bin/sh
set -e

python3 manage.py migrate --fake-initial --no-input;
if [ ! -d /opt/webtetrado/supervisor ];
then
    mkdir -p /opt/webtetrado/supervisor
fi

if [ ! -d /opt/webtetrado/logs/celery ];
then
    mkdir -p /opt/webtetrado/logs/celery
fi

cd /opt/webtetrado/;
python3 manage.py collectstatic --no-input;
cp /opt/webtetrado/public/* /opt/webtetrado/static/
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@admin.com', 'admin') if User.objects.all().count()==0 else None" | python3 manage.py shell;

exec supervisord -n -c /etc/supervisord.conf

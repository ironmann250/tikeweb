release: python manage.py migrate
release: python manage.py collectstatic
web: gunicorn tikeweb.wsgi --log-file -

web: gunicorn -w 3 manage.wsgi:application --timeout 15
release: python manage.py collectstatic --noinput && python manage.py migrate
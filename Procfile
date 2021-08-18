release: python manage.py makemigrations users
release: python manage.py makemigrations api
release: python manage.py migrate --no-input

web: gunicorn gm-soft-backend.wsgi
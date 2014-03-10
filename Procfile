web: newrelic-admin run-program waitress-serve --port=$PORT cascade.wsgi:application
worker: newrelic-admin run-program python manage.py rqworker
celery: newrelic-admin run-program python manage.py celery worker -A cascade


release: python pingpenguins/manage.py migrate
web: gunicorn --pythonpath pingpenguins pingpenguins.wsgi --log-file -
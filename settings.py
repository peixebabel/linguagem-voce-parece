import django_heroku
import os

django_heroku.settings(locals())
os.environ['STATIC_ROOT']='staticfiles'

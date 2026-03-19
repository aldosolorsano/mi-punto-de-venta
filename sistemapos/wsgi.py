import os
import pymysql  # <--- Agregamos esto
pymysql.install_as_MySQLdb() # <--- Y esto

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistemapos.settings')

application = get_wsgi_application()
app = application

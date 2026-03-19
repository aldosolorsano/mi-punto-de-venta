import pymysql

# 1. Le decimos a Django que use pymysql
pymysql.install_as_MySQLdb()

# 2. Engañamos al detector de versiones de la librería
pymysql.version_info = (2, 2, 1, 'final', 0)

# 3. Apagamos el detector de versiones de la base de datos (para que acepte tu XAMPP)
from django.db.backends.base.base import BaseDatabaseWrapper
BaseDatabaseWrapper.check_database_version_supported = lambda self: None

# 4. NUEVO: Le decimos a Django que NO use la palabra 'RETURNING' (porque MariaDB 10.4 no la conoce)
from django.db.backends.mysql.features import DatabaseFeatures
DatabaseFeatures.can_return_columns_from_insert = False
DatabaseFeatures.can_return_rows_from_bulk_insert = False
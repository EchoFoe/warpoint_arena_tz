DEBUG = False
ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db',
        'USER': 'warpoint',
        'PASSWORD': 'warpoint',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

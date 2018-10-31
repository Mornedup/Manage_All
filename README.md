
```
docker-compose build
docker-compose up -d
```

Issue was with the migrations

ALLOWED_HOSTS



## Postgress

brew services start postgresql

psql postgres

CREATE DATABASE manage_all_db;
CREATE USER managealluser WITH ENCRYPTED PASSWORD 'C5tGTaP56FG9h9qk';
GRANT ALL PRIVILEGES ON DATABASE manage_all_db TO managealluser;

Local settings:

```
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'manage_all_db',
            'USER': 'managealluser',
            'PASSWORD': 'C5tGTaP56FG9h9qk',
            'HOST': '127.0.0.1',  # set in docker-compose.yml
            'PORT': 5432  # default postgres port
        }
    }
    ```
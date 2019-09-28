## Local development

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```
CREATE DATABASE solarcity;
CREATE USER solarcity_admin WITH PASSWORD 'solarcity_admin';
GRANT ALL PRIVILEGES ON DATABASE solarcity TO solarcity_admin;
```

## Docker

```
sudo docker-compose up -d --build --force-recreate && \
sudo docker exec -it solarcity_app_1 python manage.py migrate && \
sudo docker exec -it solarcity_app_1 python manage.py collectstatic --no-input --clear
```


## Nginx
```
server {
    listen 80;
    server_name solarcity.doubletapp.ru;

    location / {
        proxy_pass http://localhost:1338;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

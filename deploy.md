# Deploy

- Use an appropriate HTTP server (e.g. gunicorn)
- Under production, ensure "DEBUG = True" is set to False in fxlab/settings.py
- Set up routes on server for the Django 'static' and 'media' directories as '/fxstatic' and '/fxmedia' respectively
- Set up file upload limits as needed to restrict uploaded image size 

Below are example configs for serving with gunicorn and routing with nginx. 


## Example of serving with gunicorn in background

``` sh
gunicorn --bind 0.0.0.0:5006 fxlab.wsgi:application --daemon
```

## Example nginx configuration

``` nginx
server {
    # ...Other blocks

    location /fxstatic/ {
        # Points to fxlab/static folder on server
        alias /var/www/html/fxlab/static/;
    }

    location /fxmedia/ {
        # Points to fxlab/media folder on server
        alias /var/www/html/fxlab/media/;
    }
    
    location /fxlab/ {
        # Limit upload size to 2 MB
        client_max_body_size 2M;

        # Redirect /fxlab to Django on port 5006
        proxy_pass http://localhost:5006/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

upstream backend {
  server localhost:10003;
}

server {
  listen 443 ssl;
	server_name yt.yuksanbo.ru;
  ssl_certificate /home/yura/Dropbox/Personal/Docs/keys/yt.yuksanbo.ru.crt;
  ssl_certificate_key /home/yura/Dropbox/Personal/Docs/keys/yt.yuksanbo.ru.key;

	location / {
    proxy_set_header X-Forwarded-Host $http_host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_http_version 1.1;

    # to proxy WebSockets in nginx
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";

    proxy_pass http://backend;
	}
}

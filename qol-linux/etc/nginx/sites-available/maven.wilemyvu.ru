server {
  listen 80;
	server_name maven.wilemyvu.ru;

  root /home/maven/repository;
	location / {
    autoindex on;
		try_files $uri $uri/ =404;
	}
}

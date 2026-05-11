FROM nginx:1.27-alpine

COPY index.html /usr/share/nginx/html/index.html
COPY app.js /usr/share/nginx/html/app.js

COPY <<EOF /etc/nginx/conf.d/default.conf
server {
  listen 80;

  location / {
    root /usr/share/nginx/html;
    index index.html;
  }

  location /api/ {
    proxy_pass http://insurance-backend:80/;
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
  }
}
EOF

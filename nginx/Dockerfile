# ベースイメージの設定
FROM nginx
COPY static /var/www/static

COPY nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;","-c","/etc/nginx/nginx.conf"]

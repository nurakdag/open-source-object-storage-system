# Nginx'in resmi imajını temel al
FROM nginx:1.25-alpine

# Varsayılan Nginx yapılandırmasını kaldır
RUN rm /etc/nginx/conf.d/default.conf

# Kendi yapılandırma dosyamızı kopyala
COPY nginx.conf /etc/nginx/nginx.conf

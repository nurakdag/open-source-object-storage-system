# 1. Build aşaması
FROM node:20-alpine as build

WORKDIR /app

# Bağımlılıkları kur
COPY package*.json ./
RUN npm install

# Proje dosyalarını kopyala
COPY . .

# Projeyi build et
RUN npm run build

# 2. Production aşaması
FROM nginx:1.25-alpine

# Build edilen dosyaları Nginx'in sunacağı dizine kopyala
COPY --from=build /app/dist /usr/share/nginx/html

# Nginx'in SPA (Single Page Application) için doğru çalışmasını sağla
# Gelen tüm istekleri index.html'e yönlendirir
COPY ../nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

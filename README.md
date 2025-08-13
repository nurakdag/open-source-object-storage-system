# Kamu Kurumları için Açık Kaynak Nesne Depolama Sistemi (AK-NDS)

Bu proje, kamu kurumlarının ve benzeri organizasyonların veri yönetimi ihtiyaçları için güvenli, ölçeklenebilir ve denetlenebilir bir açık kaynak nesne depolama sistemi MVP (Minimum Viable Product) sürümüdür.

## Hedef Mimari

Sistem, mikroservis mimarisi üzerine kurulmuştur ve aşağıdaki bileşenlerden oluşur:

- **Gateway (Nginx/Traefik):** Gelen istekleri ilgili servislere yönlendiren ters proxy.
- **Auth Service (FastAPI):** JWT tabanlı kimlik doğrulama ve rol bazlı yetkilendirme (ADMIN, USER).
- **Storage Service (FastAPI):** MinIO üzerinde nesne depolama işlemleri, `pre-signed` URL yönetimi ve mantıksal versiyonlama.
- **Audit Service (FastAPI):** RabbitMQ üzerinden gelen olayları dinleyerek denetim kayıtlarını PostgreSQL veritabanına yazar.
- **Web Admin (React/Vite):** Kullanıcıların sistemi yönetebileceği web arayüzü.
- **Altyapı (Docker Compose):** PostgreSQL, Redis, RabbitMQ ve MinIO gibi temel altyapı servisleri.

## Hızlı Başlangıç

Projenin tüm bileşenlerini tek bir komutla ayağa kaldırmak için:

```bash
# 1. Ortam değişkenlerini yapılandırın
cp .env.example .env

# 2. Docker Compose ile sistemi başlatın
docker compose -f deploy/docker-compose.yml up --build -d
```

## Paneller ve URL'ler

- **API Gateway:** `http://localhost:8000`
- **MinIO Console:** `http://localhost:9001` (Access Key: `minio`, Secret Key: `minio123`)
- **RabbitMQ Management:** `http://localhost:15672` (Kullanıcı: `guest`, Şifre: `guest`)
- **Web Admin:** `http://localhost:3000`

Daha fazla bilgi için `docs` klasöründeki belgelere ve her servisin kendi `README.md` dosyasına bakınız.

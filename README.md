# Kamu Kurumları için Açık Kaynak Nesne Depolama Sistemi (MVP)

Bu proje, kamu kurumlarının ihtiyaçları düşünülerek geliştirilmiş, açık kaynak kodlu bir nesne depolama sisteminin minimum viable product (MVP) versiyonudur. Python/FastAPI ve React kullanılarak modern bir mikroservis mimarisiyle tasarlanmıştır.

## Hedef Mimari

- **Gateway**: Nginx tabanlı reverse proxy.
- **Servisler**:
  - `auth-service`: JWT tabanlı kimlik doğrulama ve rol yönetimi (ADMIN, USER).
  - `storage-service`: MinIO üzerinden nesne işlemleri, bucket yönetimi ve pre-signed URL desteği.
  - `audit-service`: RabbitMQ üzerinden gelen olayları dinleyerek PostgreSQL'e kaydeden denetim servisi.
- **Altyapı**: Docker Compose ile yönetilen PostgreSQL, Redis, RabbitMQ ve MinIO.
- **Frontend**: React (Vite + TypeScript) ile geliştirilmiş, modern ve kullanıcı dostu bir arayüz.

## Tek Komutla Çalıştırma

Projeyi ayağa kaldırmak için Docker ve Docker Compose'un sisteminizde kurulu olması gerekmektedir.

1.  **Ortam Değişkenlerini Ayarlayın:**
    `.env.example` dosyasını kopyalayarak `.env` adında yeni bir dosya oluşturun ve içindeki değişkenleri kendi ortamınıza göre düzenleyin.

    ```bash
    cp .env.example .env
    ```

2.  **Docker Compose ile Servisleri Başlatın:**
    Aşağıdaki komut ile tüm servisleri ve altyapı bileşenlerini başlatabilirsiniz.

    ```bash
    docker compose -f deploy/docker-compose.yml up --build -d
    ```

## Erişilebilir Paneller ve URL'ler

- **Web Arayüzü**: [http://localhost](http://localhost)
- **MinIO Console**: [http://localhost:9001](http://localhost:9001)
  - **Kullanıcı Adı**: `minio`
  - **Şifre**: `minio123`
- **RabbitMQ Yönetim Paneli**: [http://localhost:15672](http://localhost:15672)
  - **Kullanıcı Adı**: `guest`
  - **Şifre**: `guest`
- **API Dökümantasyonları (Swagger)**:
  - **Auth Service**: [http://localhost/api/auth/docs](http://localhost/api/auth/docs)
  - **Storage Service**: [http://localhost/api/storage/docs](http://localhost/api/storage/docs)
  - **Audit Service**: [http://localhost/api/audit/docs](http://localhost/api/audit/docs)

## Örnek Kullanıcı Bilgileri

- **Admin Kullanıcısı**:
  - **E-posta**: `admin@demo.gov.tr`
  - **Şifre**: `Admin!234`
- **Standart Kullanıcı**:
  - **E-posta**: `user@demo.gov.tr`
  - **Şifre**: `User!234`

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.

import json
from minio import Minio
from datetime import timedelta
import pika
from .config import settings

# MinIO Client
minio_client = Minio(
    settings.MINIO_ENDPOINT.replace("http://", ""),
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False # MVP için http kullanıyoruz
)

# RabbitMQ Publisher
def get_rabbitmq_connection():
    return pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))

def publish_event(event_type: str, data: dict):
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        # Exchange ve kuyrukları deklare et (idempotent)
        channel.exchange_declare(exchange='storage_events', exchange_type='topic', durable=True)
        
        routing_key = f"storage.{event_type}"
        message = json.dumps(data)
        
        channel.basic_publish(
            exchange='storage_events',
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        print(f" [x] Sent {routing_key}:{message}")
        connection.close()
    except Exception as e:
        # Gerçek bir uygulamada burada daha iyi bir hata yönetimi ve yeniden deneme mekanizması olmalı
        print(f"RabbitMQ'ya event gönderilemedi: {e}")

import pika
import json
import time
import threading
import logging
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import SessionLocal
from .config import settings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db():
    return SessionLocal()

def callback(ch, method, properties, body):
    logging.info(f"Received event from routing key '{method.routing_key}': {body.decode()}")
    try:
        data = json.loads(body)
        db = get_db()
        
        event_type = method.routing_key.split('.')[-1]
        
        log_entry = schemas.AuditLogCreate(
            event_type=event_type,
            principal=data.get("user", "unknown"),
            details=data
        )
        crud.create_audit_log(db, log=log_entry)
        logging.info(f"Logged event: {log_entry.event_type} for user {log_entry.principal}")
    except Exception as e:
        logging.error(f"Error processing message: {e}", exc_info=True)
    finally:
        if 'db' in locals() and db:
            db.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    while True:
        try:
            connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
            channel = connection.channel()

            exchange_name = 'storage_events'
            channel.exchange_declare(exchange=exchange_name, exchange_type='topic', durable=True)

            queue_name = 'audit_log_queue'
            channel.queue_declare(queue=queue_name, durable=True)

            routing_key = 'storage.*'
            channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
            
            logging.info(f"Waiting for logs on queue '{queue_name}'. To exit press CTRL+C")
            channel.basic_consume(queue=queue_name, on_message_callback=callback)
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            logging.error(f"Connection failed, retrying in 5 seconds... Error: {e}")
            time.sleep(5)
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}. Restarting consumer...", exc_info=True)
            time.sleep(5)

def run_consumer_in_thread():
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()

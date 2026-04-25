from app.workers.celery_app import celery_app
from app.services.email_service import fetch_email_attachments
from app.workers.tasks import process_document
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)


@celery_app.task
def check_email_and_process():

    # 🔒 Prevent parallel execution
    if redis_client.get("email_lock"):
        print("⛔ Email task already running, skipping...")
        return

    redis_client.set("email_lock", "1", ex=50)

    try:
        filenames = fetch_email_attachments()

        for file in filenames:
            process_document.delay(file)

    finally:
        redis_client.delete("email_lock")
from celery import Celery

# ✅ Create Celery app
celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=[
        "app.workers.tasks",
        "app.workers.email_tasks"
    ]
)

# ✅ Queue routing (IMPORTANT)
celery_app.conf.task_routes = {
    "app.workers.tasks.process_document": {"queue": "processing"},
    "app.workers.email_tasks.check_email_and_process": {"queue": "email"},
}

# ✅ Default queue (safety)
celery_app.conf.task_default_queue = "processing"

# ✅ Beat scheduler (email trigger every 1 min)
celery_app.conf.beat_schedule = {
    "check-email-every-1-min": {
        "task": "app.workers.email_tasks.check_email_and_process",
        "schedule": 60.0,
    },
}

# ✅ Timezone
celery_app.conf.timezone = "Asia/Kolkata"

# ✅ Stability settings
celery_app.conf.task_acks_late = True
celery_app.conf.worker_prefetch_multiplier = 1

# ✅ Serialization (prevents bugs)
celery_app.conf.task_serializer = "json"
celery_app.conf.accept_content = ["json"]
import os
from celery import Celery

app = Celery('tasks',
             broker=os.environ.get('CELERY_BROKER_URL'),
             backend=os.environ.get('CELERY_RESULT_BACKEND'))

app.conf.update(
    result_expires=3600,
    # Add other configurations as needed
)

if __name__ == '__main__':
    app.start()

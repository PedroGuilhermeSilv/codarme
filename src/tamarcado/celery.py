from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.tamarcado.settings.prod')
app = Celery('tasks', broker='redis://redis:6379/0')

app.autodiscover_tasks()

@app.task()
def soma(x, y):
    return x + y
from celery import Celery
from fastapi import FastAPI

app = FastAPI()
celery_app = Celery(
    "tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/1"
)

def main() -> int:
    import multiprocessing

    import uvicorn

    process_celery = multiprocessing.Process(
        target=lambda: celery_app.worker_main(["worker", "-l", "info"])
    )
    process_uvicorn = multiprocessing.Process(
        target=lambda: uvicorn.run(app, host="127.0.0.1", port=8000)
    )
    process_celery.start()
    process_uvicorn.start()
    process_celery.join()
    process_uvicorn.join()
    return 0
import asyncio
import logging
import threading
import time

from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    logging.basicConfig(level=logging.INFO)
    logging.info("App started")


@app.get("/async_sleep")
async def async_sleep():
    logging.info("async_sleep: Sleeping for 10 seconds")
    await asyncio.sleep(10)
    logging.info("async_sleep: Slept for 10 seconds")
    return {"message": "async_sleep"}


@app.get("/sync_sleep")
def sync_sleep():
    logging.info("sync_sleep: Sleeping for 10 seconds")
    time.sleep(10)
    logging.info("sync_sleep: Slept for 10 seconds")
    return {"message": "sync_sleep"}


@app.get("/background_task")
def background_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(sync_sleep)
    return {"message": "background_task"}


@app.get("/thread_task")
def thread_task():
    def sync_sleep():
        logging.info("threading: Sleeping for 10 seconds")
        time.sleep(10)
        logging.info("threading: Slept for 10 seconds")

    threading.Thread(target=sync_sleep, daemon=False).start()
    return {"message": "threading"}


@app.get("/async_tasks")
async def async_tasks():

    logging.info(await asyncio.gather(async_sleep(), async_sleep(), async_sleep()))
    return {"message": "async_tasks"}

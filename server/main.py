import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from server.api.routes import router
from server.queue.worker import moderation_worker


@asynccontextmanager
async def lifespan(app: FastAPI):
    worker_task = asyncio.create_task(moderation_worker())

    yield

    worker_task.cancel()


app = FastAPI(
    title="Inteligentna komponenta",
    lifespan=lifespan
)

app.include_router(router, prefix="/api")
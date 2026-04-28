import asyncio
import uuid
from dataclasses import dataclass

@dataclass
class ModerationJob:
    job_id: str
    filename: str
    image_bytes: bytes
    future: asyncio.Future

moderation_queue: asyncio.Queue[ModerationJob] = asyncio.Queue()

def create_job(filename: str, image_bytes: bytes) -> ModerationJob:
    loop = asyncio.get_running_loop()
    return ModerationJob(
        job_id = str(uuid.uuid4()),
        filename = filename,
        image_bytes = image_bytes,
        future = loop.create_future()
    )
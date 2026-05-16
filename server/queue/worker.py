from pathlib import Path
from PIL import Image
from io import BytesIO

from server.queue.moderation_queue import moderation_queue
from inteligent_component.moderation import moderate_image
from inteligent_component.config import load_config


DEFAULT_CONFIG_DIR = Path("inteligent_component/config")

# Config se naloži enkrat ob zagonu workerja
config = load_config(DEFAULT_CONFIG_DIR)

async def moderation_worker():
    while True:
        job = await moderation_queue.get()

        try:
            image = Image.open(BytesIO(job.image_bytes)).convert("RGB")

            result = moderate_image(image, config)

            job.future.set_result(
                {
                    "job_id": job.job_id,
                    "filename": job.filename,
                    "result": result
                }
            )

        except Exception as e:
            job.future.set_exception(e)

        finally:
            moderation_queue.task_done()
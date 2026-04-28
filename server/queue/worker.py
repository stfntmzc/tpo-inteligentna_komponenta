from PIL import Image
from io import BytesIO

from server.queue.moderation_queue import moderation_queue
from inteligent_component.moderation import moderate_image


async def moderation_worker():
    while True:
        job = await moderation_queue.get()

        try:
            image = Image.open(BytesIO(job.image_bytes)).convert("RGB")

            result = moderate_image(image)

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
__all__ = ("broker",)

from taskiq_aio_pika import AioPikaBroker

from core.config import settings

broker = AioPikaBroker(
    # url="amqp://guest:guest@192.168.0.104:5672//",
    url=settings.taskiq.url,
)

from faststream.rabbit import RabbitQueue, Channel
from core.models.rabbitmq.base import rabbitmq_router, direct_exchenge


simple_email_queue = RabbitQueue("send-simple-email-queue")
simple_email_chennel = Channel(2)
simple_email_publisher = rabbitmq_router.publisher(simple_email_queue, direct_exchenge)
simple_email_subscriber = rabbitmq_router.subscriber(
    simple_email_queue, direct_exchenge, channel=simple_email_chennel
)

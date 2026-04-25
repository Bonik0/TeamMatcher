from faststream.rabbit import RabbitQueue
from core.models.rabbitmq.base import rabbitmq_router, direct_exchenge


auth_verify_queue = RabbitQueue("auth-verify-queue")
auth_verify_publisher = rabbitmq_router.publisher(auth_verify_queue, direct_exchenge)
auth_verify_subscriber = rabbitmq_router.subscriber(auth_verify_queue, direct_exchenge)

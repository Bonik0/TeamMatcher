from faststream.rabbit.fastapi import RabbitRouter
from faststream.rabbit import RabbitExchange, ExchangeType
from .config import get_url


rabbitmq_router = RabbitRouter(get_url())


direct_exchenge = RabbitExchange("direct_exch")
topic_exchange = RabbitExchange("topic_exch", ExchangeType.TOPIC)

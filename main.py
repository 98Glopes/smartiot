import logging

from micro_framework.amqp.entrypoints import EventListener
from micro_framework.routes import Route
from micro_framework.runner import Runner

config = {
    'AMQP_URI': 'amqps://gquorlsc:UE-n6Zn0AA3yddcyY_nqiFG0nUOML7k5@grouse.rmq.cloudamqp.com/gquorlsc',
    'MAX_WORKERS': 3,
    'SERVICE_NAME': 'smartiot_service',
    'MAX_TASKS_PER_CHILD': 2, # currently for process WORKER_MODE only
    'WORKER_MODE': 'thread',

}

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')

routes = [
    Route(
        'services.collector.Collector',
        method_name='insert_data_from_mqtt', # If not provided, the __call__ method is called
        entrypoint=EventListener(
            source_service='my_service', event_name='event_name',
        ),
    ),
]

if __name__ == '__main__':
    runner = Runner(routes, config)
    runner.start()

import copy
import logging
import sys
import time

import colorama
import pika
from python_logging_rabbitmq import RabbitMQHandler, RabbitMQHandlerOneWay
from r00auth import config
from r00helper.asession import global_session_id

LOG_COLORS = {
    logging.DEBUG: colorama.Fore.WHITE,
    logging.INFO: colorama.Fore.LIGHTBLUE_EX,
    logging.WARNING: colorama.Fore.YELLOW,
    logging.CRITICAL: colorama.Fore.LIGHTRED_EX,
    logging.FATAL: colorama.Fore.LIGHTRED_EX,
    logging.ERROR: colorama.Fore.LIGHTRED_EX,
}


class ColorFormatter(logging.Formatter):
    def format(self, record, *args, **kwargs):
        new_record = copy.copy(record)
        if new_record.levelno in LOG_COLORS:
            new_record.levelname = "{color_begin}{level}{color_end}".format(
                level=f'{new_record.levelname:<8}',
                color_begin=LOG_COLORS[new_record.levelno],
                color_end=colorama.Style.RESET_ALL,
            )
        return super(ColorFormatter, self).format(new_record)


def _create_handler_steam():
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = ColorFormatter("%(levelname)s | %(asctime)s | %(message)s", "%H:%M:%S")
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    return handler


def _create_handler_rabbit(session_id):
    login = config.rabbitmq.login
    password = config.rabbitmq.password
    hostname = config.rabbitmq.hostname
    port = config.rabbitmq.port

    credentials = pika.PlainCredentials(login, password)
    conn_params = pika.ConnectionParameters(hostname, port, credentials=credentials)
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()

    formatter = logging.Formatter(
        fmt='%(levelname)-8s | %(asctime)s | %(message)s',
        datefmt="%H:%M:%S")

    channel.queue_declare(queue=session_id, durable=False)
    channel.exchange_declare(exchange='log', exchange_type='direct', durable=False)
    channel.queue_bind(exchange='log', queue=session_id, routing_key=session_id)

    return RabbitMQHandler(host=hostname, port=port, username=login, password=password,
                                          level=logging.DEBUG,
                                          routing_key_formatter=lambda r: session_id,
                                          declare_exchange=False,
                                          formatter=formatter)


_colorama = colorama.init(convert=True)
log = logging.getLogger('test')
log.setLevel(logging.DEBUG)
log.addHandler(_create_handler_steam())
log.addHandler(_create_handler_rabbit(global_session_id))
log.propagate = False

if __name__ == '__main__':
    t0 = time.time()
    log.debug("Hi")
    log.info("Hi")
    log.warning("Hi")
    log.error("Hi")
    print(time.time() - t0)

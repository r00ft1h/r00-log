import logging
import sys
import colorama
import copy

import jmespath

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
    #formatter = ColorFormatter("%(levelname)s %(threadName)s %(module)s %(funcName)s -> %(message)s")
    #self.steam_handler_format = logging.Formatter("%(levelname)s %(funcName)s -> %(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    return handler


def _create_handler_rabbit(self, filename):
    with open('')
    login = jmespath.search("services.rabbitmq.login", project.configdata)
    password = jmespath.search("services.rabbitmq.password", project.configdata)
    hostname = jmespath.search("services.rabbitmq.hostname", project.configdata)
    port = jmespath.search("services.rabbitmq.port", project.configdata)

    credentials = pika.PlainCredentials(login, password)
    conn_params = pika.ConnectionParameters(hostname, port, credentials=credentials)
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()

    channel.queue_declare(queue=filename, durable=False)
    channel.exchange_declare(exchange='log', exchange_type='direct', durable=False)
    channel.queue_bind(exchange='log', queue=filename, routing_key=filename)

    self.rabbit_handler = RabbitMQHandler(host=hostname, port=port, username=login, password=password,
                                          level=logging.DEBUG,
                                          routing_key_formatter=lambda r: filename,
                                          declare_exchange=False,
                                          formatter=self.formatter)

    # channel.close()
    # connection.close()


_colorama = colorama.init(convert=True)
log = logging.getLogger('test')
log.setLevel(logging.DEBUG)
log.addHandler(_create_handler_steam())
log.propagate = False

if __name__ == '__main__':
    log.debug("Hi")
    log.info("Hi")
    log.warning("Hi")
    log.error("Hi")

# import copy
# import os
# import sys
# import tempfile
# import threading
# import time
# from pathlib import Path
# from queue import Queue
#
# import jmespath
# import pika
# #import sentry_sdk
# from python_logging_rabbitmq import RabbitMQHandler
# # from sentry_sdk.integrations.logging import LoggingIntegration
#
# from config import NAME_RUN, PROJECT_PY
# from config.init import project
#
#
# LOG_COLORS = {
#     logging.ERROR: colorama.Fore.LIGHTRED_EX,
#     logging.WARNING: colorama.Fore.YELLOW,
#     logging.INFO: colorama.Fore.LIGHTBLUE_EX
# }
#
# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger('asyncio').setLevel(logging.INFO)
# logging.getLogger('urllib3').setLevel(50)
# logging.getLogger('urllib3.socks').setLevel(50)
# logging.getLogger('urllib3.contrib.socks').setLevel(50)
# logging.getLogger('googleapiclient').setLevel(50)
# logging.getLogger('oauth2client').setLevel(50)
# logging.getLogger('telegram').setLevel(50)
# logging.getLogger('PIL').setLevel(50)
# logging.getLogger('pika').setLevel(50)
# logging.getLogger('webdav3.client').setLevel(50)
# logging.getLogger('pyaxmlparser').setLevel(50)
# logging.getLogger('pyaxmlparser').setLevel(50)
# logging.getLogger('geocoder').setLevel(50)
# logging.getLogger('telethon').setLevel(50)
# logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(50)
#
#
# class Indent:
#     def __init__(self):
#         self._deep = 0
#         self._space = 4
#         self._fmt = "."
#
#     @property
#     def deep(self):
#         return self._deep
#
#     @deep.setter
#     def deep(self, value):
#         self._deep = value
#
#     @property
#     def space(self):
#         return (self._space * self._deep) * self._fmt
#
#     @property
#     def fmt(self):
#         return self._fmt
#
#
# class LogProxy:
#     def __init__(self, logger):
#         self.log = logger
#         self.stack = Queue()
#
#     def start(self):
#         th = threading.Thread(target=self._run)
#         th.daemon = False
#         th.name = 'LogProxy'
#         th.start()
#
#     def _run(self):
#         while True:
#             if not self.stack.empty():
#                 func, msg = self.stack.queue.popleft()
#                 func(msg)
#             else:
#                 for th in threading.enumerate():
#                     if th.name == "MainThread":
#                         if not th.is_alive():
#                             time.sleep(3)
#                             return True
#                 time.sleep(1)
#
#
#     def debug(self, msg):
#         self.stack.queue.append((getattr(self.log, "debug"), f"{log_indent.space}{str(msg)}"))
#
#     def info(self, msg):
#         self.stack.queue.append((getattr(self.log, "info"), f"{log_indent.space}{str(msg)}"))
#
#     def warning(self, msg):
#         self.stack.queue.append((getattr(self.log, "warning"), f"{log_indent.space}{str(msg)}"))
#
#     def error(self, msg):
#         self.stack.queue.append((getattr(self.log, "error"), f"{log_indent.space}{str(msg)}"))
#         raise ValueError(msg)
#
#
# class LogInit:
#     def __init__(self):
#         self.colorama = colorama.init(convert=True)
#         self.steam_handler = None
#         self.file_handler = None
#         self.rabbit_handler = None
#         self.dirpath = Path(__file__).parent
#         self.formatter = None
#         self.logger_host = None
#
#     def _wait_project_host(self):
#         # Ждем установку project.host либо устанавливаем доступ к логам на 192.168.1.555
#         project.host = None
#         t0 = time.time()
#         while time.time() - t0 < 20:
#             if project.host:
#                 host = project.host
#                 break
#             time.sleep(0.1)
#         else:
#             print(f'Elapsed wait init log: {time.time() - t0}')
#             host = '192.168.1.999'
#
#         self._create_file_handler()
#         self._create_steam_handler()
#         self._create_rabbit_handler(host)
#         logger = self._create_logger(host)
#         log_proxy = LogProxy(logger)
#         log_proxy.start()
#         self.logger_host = log_proxy
#         self.logger_host.info("first message")
#         print("Logger init host OK", host)
#         return True
#
#     def create_logger(self):
#         threading.Thread(target=self._wait_project_host, daemon=True).start()
#
#     @staticmethod
#     def connect_sentry():
#         sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)
#         sentry_sdk.init(dsn="https://6e1fc8e6dd54451fa5c017f2d0d17b0a@o421508.ingest.sentry.io/5341421",
#                         integrations=[sentry_logging])
#
#     def _create_steam_handler(self):
#         self.steam_handler = logging.StreamHandler(stream=sys.stdout)
#         formatter = ColorFormatter("%(levelname)s | %(message)s")
#         #formatter = ColorFormatter("%(levelname)s %(threadName)s %(module)s %(funcName)s -> %(message)s")
#         #self.steam_handler_format = logging.Formatter("%(levelname)s %(funcName)s -> %(message)s")
#         self.steam_handler.setFormatter(formatter)
#         self.steam_handler.setLevel(logging.DEBUG)
#
#     def _create_file_handler(self):
#         _, filepath = tempfile.mkstemp()
#         self.file_handler = logging.FileHandler(filepath, mode='w', encoding='utf-8')
#         self.formatter = logging.Formatter(
#             fmt='%(levelname)-7s | %(asctime)s | %(message)s',
#             # fmt='%(levelname)-7s | %(asctime)s | %(threadName)-11s | %(module)-13s | %(funcName)-20s | %(message)s',
#             datefmt="%H:%M:%S")
#         self.file_handler.setFormatter(self.formatter)
#         self.file_handler.setLevel(logging.DEBUG)
#
#     def _create_logger(self, filename):
#         log = logging.getLogger(filename)
#         log.setLevel(logging.DEBUG)
#         log.addHandler(self.steam_handler)
#         log.addHandler(self.file_handler)
#         log.addHandler(self.rabbit_handler)
#         log.propagate = False
#         return log
#
#     def _create_rabbit_handler(self, filename):
#         login = jmespath.search("services.rabbitmq.login", project.configdata)
#         password = jmespath.search("services.rabbitmq.password", project.configdata)
#         hostname = jmespath.search("services.rabbitmq.hostname", project.configdata)
#         port = jmespath.search("services.rabbitmq.port", project.configdata)
#
#         credentials = pika.PlainCredentials(login, password)
#         conn_params = pika.ConnectionParameters(hostname, port, credentials=credentials)
#         connection = pika.BlockingConnection(conn_params)
#         channel = connection.channel()
#
#         channel.queue_declare(queue=filename, durable=False)
#         channel.exchange_declare(exchange='log', exchange_type='direct', durable=False)
#         channel.queue_bind(exchange='log', queue=filename, routing_key=filename)
#
#         self.rabbit_handler = RabbitMQHandler(host=hostname, port=port, username=login, password=password,
#                                               level=logging.DEBUG,
#                                               routing_key_formatter=lambda r: filename,
#                                               declare_exchange=False,
#                                               formatter=self.formatter)
#
#         # channel.close()
#         # connection.close()
#
#
# class ColorFormatter(logging.Formatter):
#     def format(self, record, *args, **kwargs):
#         new_record = copy.copy(record)
#         if new_record.levelno in LOG_COLORS:
#             new_record.levelname = "{color_begin}{level}{color_end}".format(
#                 level=f'{new_record.levelname:^5}',
#                 color_begin=LOG_COLORS[new_record.levelno],
#                 color_end=colorama.Style.RESET_ALL,
#             )
#         return super(ColorFormatter, self).format(new_record)
#
#
# class log:
#     last_text = ""
#     prefix = ''
#
#     def _select(func):
#         def magic(text_log):
#             logger = logging if not _log_init.logger_host else _log_init.logger_host
#             # if log.last_text == text_log:
#             #     return None
#             log.last_text = text_log
#             return func(logger, text_log)
#         return magic
#
#     @_select
#     def debug(_logger, text):
#         if log.prefix: text = '[' + log.prefix + '] ' + text
#         return getattr(_logger, "debug")(text)
#
#     @_select
#     def info(_logger, text):
#         if log.prefix: text = '[' + log.prefix + '] ' + text
#         return getattr(_logger, "info")(text)
#
#     @_select
#     def warning(_logger, text):
#         if log.prefix: text = '[' + log.prefix + '] ' + text
#         return getattr(_logger, "warning")(text)
#
#     @_select
#     def error(_logger, text):
#         if log.prefix: text = '[' + log.prefix + '] ' + text
#         return getattr(_logger, "error")(text)
#
#
# os.chdir(Path(__file__).parent)
# _log_init = LogInit()
# _log_init.create_logger()
# log_indent = Indent()
#
#
# if __name__ == '__main__':
#     project.host = "192.168.1.204"
#
#     while True:
#         for i in range(10):
#             log.info(i)
#         time.sleep(1)
#
#         import logging
#
#         loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
#         print(loggers)
#

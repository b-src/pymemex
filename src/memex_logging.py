import logging

memex_logger = logging.getLogger("MEMEXLOGGER")
memex_logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

memex_logger.addHandler(handler)

import logging

logger = logging.getLogger("stream")
handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("Logger Initialized")

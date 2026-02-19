import logging
import os


# Logger Setup
def setup_logger(name: str = "trading_bot") -> logging.Logger:
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler("logs/trading_bot.log")  # Logs Stored in file.
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)

    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger

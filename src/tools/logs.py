import logging


def create_log(level: str):

    log_level = logging.INFO

    if level == "INFO":
        log_level = logging.INFO
    elif level == "DEBUG":
        log_level = logging.DEBUG

    log_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)7s | %(filename)-10s:%(lineno)-4s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # create console handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(log_level)
    consoleHandler.setFormatter(log_formatter)

    # Add console handler to logger
    logger.addHandler(consoleHandler)

    logger.info("================> Running sensor <================")

    return logger

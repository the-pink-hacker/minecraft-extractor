import logging


def get_logger(*args: str):
    blue = "\x1b[34m"
    reset = "\x1b[0m"
    separator = f"{reset}/{blue}"
    return logging.getLogger(f"{separator.join(args)}{reset}")

import logging
import sys

try:
    import PySimpleGUI as sg                #  Better than CTRL+c
except ImportError:
    sg = NotImplemented

# Force this if you want no graphical windows' interface, even with PySimpleGUI and TK installed.
# Commented = windows, uncommented = text only
#sg = NotImplemented

# Global logger
def setup_logger (name):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[PID %(process)d %(asctime)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def MyLog (logger, log_string):
    logger.info(log_string)
    sys.stdout.flush()

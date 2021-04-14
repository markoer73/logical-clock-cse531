#
#   Util.py
#
# Marco Ermini - March 2021 for ASU CSE531 Course
# Do not leech!
# Built with python 3.8 with GRPC and GRPC-tools libraries; may work with other Python versions
'''Utility classes - logging, Windows manager, etc.'''

import logging
import sys

import banking_pb2
import banking_pb2_grpc

try:
    import PySimpleGUI as sg                #  Better than CTRL+c
except ImportError:
    sg = NotImplemented

# Force this if you want no graphical windows' interface, even with PySimpleGUI and TK installed.
# Commented = windows, uncommented = text only
sg = NotImplemented

# Global logger
def setup_logger (name):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[PID %(process)d %(asctime)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def MyLog (logger, log_string, window=None):
    logger.info(log_string)
    sys.stdout.flush()
    if (sg != NotImplemented):
        if (window != None):
            print(
                ResponseText
            )
            window.Refresh()


# Utility functions, used for readability
#
def get_operation(operation):
    """Returns the message type from the operation described in the input file."""
    if operation == 'query':
        return banking_pb2.QUERY
    if operation == 'deposit':
        return banking_pb2.DEPOSIT
    if operation == 'withdraw':
        return banking_pb2.WITHDRAW

def get_operation_name(operation):
    """Returns the operation type from the message."""
    if operation == banking_pb2.QUERY:
        return 'QUERY'
    if operation == banking_pb2.DEPOSIT:
        return 'DEPOSIT'
    if operation == banking_pb2.WITHDRAW:
        return 'WITHDRAW'

def get_result_name(name):
    """Return state of a client's operation."""
    if name == banking_pb2.SUCCESS:
        return 'SUCCESS'
    if name == banking_pb2.FAILURE:
        return 'FAILURE'
    if name == banking_pb2.ERROR:
        return 'ERROR'
"""
This logger is used inside handlers to log stuff happening inside.
Mainly will be used by developers on that framework.
"""
import logging

handler_logger = logging.getLogger("storm:handler")

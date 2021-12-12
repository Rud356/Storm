"""
This logger is used internally for logging what event happened,
what error wasn't handled or occurred during working on event events handling.
This includes unexpected errors that wasn't caught by handlers, start and
end of events handling.
"""
import logging

events_logger = logging.getLogger("storm:events_logger")

# logging_system.py - New module for logging game events
import logging
from constants import LOG_LEVEL_INFO

class LoggingSystem:
    """
    Handles game logging.
    """
    def __init__(self, level=LOG_LEVEL_INFO):
        logging.basicConfig(level=level, filename='game.log', filemode='w')
        self.logger = logging.getLogger('game')

    def log_event(self, message):
        self.logger.info(message)

    def log_frame_stats(self, fps):
        self.logger.debug(f"FPS: {fps}")

    def close(self):
        logging.shutdown()

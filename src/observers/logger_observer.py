import logging

from src.observers.events.base import BaseEvent
from src.utils.abstract.observer import Observer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class LoggerObserver(Observer):
    def accept(self, event: BaseEvent):
        logger.info(str(event.model_dump()))

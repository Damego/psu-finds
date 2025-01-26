from abc import ABC, abstractmethod


class Observer[T](ABC):
    @abstractmethod
    def accept(self, event: T):
        raise NotImplementedError

from abc import ABCMeta, abstractmethod
from .exceptions import ObserverNotFound


class Observer(metaclass=ABCMeta):

    @abstractmethod
    def add(self, message: str) -> None:
        pass


class Observable(metaclass=ABCMeta):

    observers = {}

    def register_observer(self, observer_type: str, observer: Observer) -> None:
        if observer_type not in self.observers:
            self.observers[observer_type] = []
        self.observers[observer_type].append(observer)

    def notify_observers(self, message: str) -> None:

        if message['meta']['type'] not in self.observers:
            raise ObserverNotFound(f"Message type: {message['meta']['type']}")

        for observer_type in self.observers:
            if message['meta']['type'] == observer_type:
                for observer in self.observers[observer_type]:
                    observer.add(message)

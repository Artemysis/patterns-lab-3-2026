from abc import ABC, abstractmethod
from pathlib import Path

from logger import (
    ConsoleOutputStrategy,
    FileOutputStrategy,
    OutputStrategy,
    UpperFileOutputStrategy,
)


class OutputStrategyCreator(ABC):
    """Базовый создатель: объявляет Factory Method для одной стратегии."""

    @abstractmethod
    def create(self, log_file: str | Path = "application.log") -> OutputStrategy:
        raise NotImplementedError


class ConsoleStrategyCreator(OutputStrategyCreator):
    def create(self, log_file: str | Path = "application.log") -> OutputStrategy:
        return ConsoleOutputStrategy()


class FileStrategyCreator(OutputStrategyCreator):
    def create(self, log_file: str | Path = "application.log") -> OutputStrategy:
        return FileOutputStrategy(log_file)


class UpperFileStrategyCreator(OutputStrategyCreator):
    def create(self, log_file: str | Path = "application.log") -> OutputStrategy:
        return UpperFileOutputStrategy(log_file)

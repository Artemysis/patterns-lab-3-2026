from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from pathlib import Path


class LogLevel(str, Enum):
    TRACE = "TRACE"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"


class OutputStrategy(ABC):
    """Интерфейс стратегии вывода отформатированного сообщения."""

    @abstractmethod
    def write(self, formatted_message: str) -> None:
        raise NotImplementedError


class ConsoleOutputStrategy(OutputStrategy):
    def write(self, formatted_message: str) -> None:
        print(formatted_message)


class FileOutputStrategy(OutputStrategy):
    def __init__(self, log_file: str | Path) -> None:
        self.log_file = Path(log_file)

    def write(self, formatted_message: str) -> None:
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with self.log_file.open("a", encoding="utf-8") as stream:
            stream.write(formatted_message + "\n")


class UpperFileOutputStrategy(OutputStrategy):
    def __init__(self, log_file: str | Path) -> None:
        self.log_file = Path(log_file)

    def write(self, formatted_message: str) -> None:
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with self.log_file.open("a", encoding="utf-8") as stream:
            stream.write(formatted_message.upper() + "\n")


class Logger:
    """Контекст Strategy. Форматирует сообщение и делегирует вывод стратегии."""

    def __init__(self, strategy: OutputStrategy) -> None:
        self.set_strategy(strategy)

    def set_strategy(self, strategy: OutputStrategy) -> None:
        if not isinstance(strategy, OutputStrategy):
            raise TypeError("Strategy должна реализовывать OutputStrategy")
        self._strategy = strategy

    def _normalize_level(self, level: LogLevel | str) -> LogLevel:
        if isinstance(level, LogLevel):
            return level

        if isinstance(level, str):
            try:
                return LogLevel(level)
            except ValueError:
                raise ValueError(f"Unknown log level: {level}") from None

        raise TypeError("Log level must be a LogLevel or a string")

    def _format(self, level: LogLevel | str, message: str) -> str:
        normalized_level = self._normalize_level(level)

        if not isinstance(message, str):
            raise TypeError("Message must be a string")

        if message == "":
            raise ValueError("Message must not be empty")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{timestamp} [{normalized_level.value}] {message}"

    def log(self, level: LogLevel | str, message: str) -> str:
        formatted = self._format(level, message)
        self._strategy.write(formatted)
        return formatted

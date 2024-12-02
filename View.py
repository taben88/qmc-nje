from abc import ABC, abstractmethod


class View(ABC):

    """Abstract base class for console and GUI views."""

    @abstractmethod
    def getMinterms(self) -> list[int]:
        ...

    @abstractmethod
    def getDontCares(self) -> list[int]:
        ...

    @abstractmethod
    def getNVars(self) -> int:
        ...

    @abstractmethod
    def outputResult(self, result: dict[str, str|list[str]|list[tuple[str, str]]]) -> None:
        ...
    
    @abstractmethod
    def outputError(self, error: Exception) -> None:
        ...

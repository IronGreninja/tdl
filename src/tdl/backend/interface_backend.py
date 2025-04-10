from abc import ABC, abstractmethod
from pathlib import Path

from .models import ListEntry


class IBackend(ABC):
    """Backend interface"""

    def __init__(self, datafile: Path) -> None:
        try:
            datafile.parent.mkdir(exist_ok=True, parents=True)
        except FileExistsError:
            print(
                f"Error creating directory {datafile.parent}. File with same name already exists!"
            )
            raise

    @abstractmethod
    def Insert(self, entry: ListEntry) -> None:
        """
        Inserts a new item
        """

    @abstractmethod
    def Read(self, ls_strat: str) -> list[ListEntry]:
        """
        ls_strat: print strategy. Can be one of -
            done: only completed items
            priority: only priority (not completed) items
            all: all items
            pending: not completed items
        """

    @abstractmethod
    def MarkDone(self, id: int, completed_on: str) -> int:
        """
        Marks an item of (id) as done on (completedOn).

        Returns:
            0 if id was updated successfully
            1 if id doesn't exist
            2 if id was already marked as done
        """

    @abstractmethod
    def ClearDone(self) -> None:
        """
        Delete done items
        """

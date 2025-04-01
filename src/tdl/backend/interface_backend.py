from abc import ABC, abstractmethod
from pathlib import Path
from .models import ListEntry, ListEntry_R


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
    def Read(self, done: bool = False, priority: bool = False) -> list[ListEntry_R]:
        """
        done: Returns only completed items
        priority: Returns only priority items
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

from abc import ABC, abstractmethod
from pathlib import Path


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
    def Insert(self, message: str, createdOn: str, priority: int) -> None:
        """
        Inserts a new item
        """

    @abstractmethod
    def Read(
        self, done: bool = False, priority: bool = False
    ) -> list[dict[str, str | None | int]]:
        """
        done: Returns only completed items
        priority: Returns only priority items

        Returns list of todo items where each row is
        {id: int, priority: int, message: str, createdOn: str, completedOn: str | None }

        if done=False, completedOn is not in dict
        """

    @abstractmethod
    def MarkDone(self, id: int, completedOn: str) -> int:
        """
        Marks an item of (id) as done on (completedOn).

        Returns:
            0 if id was updated successfully
            1 if id doesn't exist
            2 if id was already marked as done
        """

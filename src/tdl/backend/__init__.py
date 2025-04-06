from .backend_csv import Bcsv
from .backend_sqlite import Bsqlite
from .interface_backend import IBackend

Backend: dict[str, type[IBackend]] = {
    "sqlite": Bsqlite,
    "csv": Bcsv,
}

__all__ = ["Backend"]

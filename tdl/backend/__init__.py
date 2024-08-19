from .backend_sqlite import Bsqlite
from .interface_backend import IBackend

Backend: dict[str, type[IBackend]] = {
    "sqlite": Bsqlite,
}

__all__ = ["Backend"]

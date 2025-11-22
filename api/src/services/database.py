import json
from logging import getLogger
from typing import TypeVar

VT = TypeVar("VT")

log = getLogger(__name__)


class JSONDatabase(dict[str, VT]):
    """
    A dictionary which operates together with a JSON file.
    Data is initially loaded from a JSON file and can be saved back to the file.
    You should not modify this class.
    """

    def __init__(self, path: str):
        """Initialize the database with the file data at the given path."""
        super().__init__()
        self._path = path

        log.info("Loading database from file")
        with open(path) as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                raise ValueError("Specified data file is not serializable.")

        if not isinstance(data, dict):
            raise ValueError("Data file does not contain a valid database.")

        self.update(data)

    def __setitem__(self, key: str, value: VT) -> None:
        if not isinstance(key, str):
            raise TypeError(f"Database key must be str, not {type(key)}")
        return super().__setitem__(key, value)

    def close(self) -> None:
        """Save database by writing to file."""
        log.info("Saving database to file")
        with open(self._path, "w") as file:
            json.dump(self, file, indent="\t")

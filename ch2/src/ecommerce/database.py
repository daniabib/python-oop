from typing import Optional


class Database:
    """The database implementation"""

    def __init__(self, connection: Optional[str] = None) -> None:
        """ Creates a connection to a database."""


db: Optional[Database] = None


def initialize_database(connection: Optional[str] = None) -> None:
    global db
    db = Database(connection)
    # print(f"initialized {db!r} with {connection!r}")


def get_database(connection: Optional[str] = None) -> Database:
    global db
    if not db:
        db = Database(connection)
        # print(f"initialized {db!r} with {connection!r}")
    return db

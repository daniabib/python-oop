import io
from typing import Protocol


class IOResource(Protocol):
    uri: str

    def __init__(self, uri: str):
        pass

    def open(self) -> int:
        pass

    def close(self) -> None:
        pass


class FileResource:

    def __init__(self, uri: str):
        self.uri = uri

    def open(self):
        self.file = io.FileIO(self.uri)
        return self.file.fileno()

    def close(self):
        self.file.close()


class CocoAmassado:
    def __init__(self, uri: str) -> None:
        self.uri = uri

    def open(self):
        print("HEY")

    def close(self):
        print("HOY")


def write_resource_to_disk(r: IOResource):
    pass


write_resource_to_disk(FileResource("file.txt"))
write_resource_to_disk(CocoAmassado("file.txt"))

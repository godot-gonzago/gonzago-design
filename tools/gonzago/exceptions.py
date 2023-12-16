from pathlib import Path


class PathError(ValueError):
    def __init__(self, path: Path, message: str = "Invalid path"):
        super().__init__(message)
        self.path = path


class PathNotFoundError(FileNotFoundError):
    def __init__(self, path: Path, message: str = "Path does not exist"):
        super().__init__(message)
        self.path = path

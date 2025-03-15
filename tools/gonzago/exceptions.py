from pathlib import Path
from typing import Optional

# class GonzagoError(Exception):
#    pass
#
#
# class PathError(ValueError, GonzagoError):
#    def __init__(self, path: Path, message: str = "Invalid path"):
#        self.path = path
#        if message is None:
#            message = "Invalid path"
#        super().__init__(message)
#
#
# class PathNotFoundError(FileNotFoundError, GonzagoError):
#    def __init__(self, path: Path, message: Optional[str] = "Path does not exist") -> None:
#        super().__init__(message)
#        self.path = path
#
#
# class ParsingError(ValueError, GonzagoError):
#    def __init__(self, file: Path, message: Optional[str] = None) -> None:
#        self._file = file
#
#        if message is None:
#            message = "Parsing error"
#
#        super().__init__(f"{message} for {file.name}")
#
#    @property
#    def file(self):
#        return self._file
#
#
# class NameConflictError(KeyError, GonzagoError):
#    def __init__(self, name: str, message: Optional[str]):
#        self._name = name
#
#        if message is None:
#            message = f'Name "{name}" already exists.'
#
#        super().__init__(message)
#
#    @property
#    def name(self):
#        return self._name
#
#
## raise when file cannot be read.
# class FileTypeError(TypeError):
#    msg: str = "File type cannot be handled"
#    file: Optional[Path]
#
#
## raise when no writer or reader could be found.
# class MissingFileHandlerError(LookupError):
#    msg: str = "No matching file handler found"
#    file: Optional[Path]
#    format: Optional[str]
#

from __future__ import annotations

from datetime import datetime
import json
import os
from pathlib import Path
import typing as t
import uuid

from red_fileops.core import DEFAULT_SCAN_RESULTS_FILE
from red_fileops.core.utils import converters
from red_fileops.sysinfo import PLATFORM, PlatformInfo

import pendulum
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    computed_field,
    field_validator,
    model_validator,
)

class ScanEntity(BaseModel):
    """Store data about a file or directory found in a scan."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    path: t.Union[str, Path] = Field(default=None)

    @computed_field
    @property
    def name(self) -> str:
        if isinstance(self.path, Path):
            return self.path.name
        elif isinstance(self.path, str):
            return f"{Path(self.path).name}"
        else:
            return None

    @computed_field
    @property
    def entity_type(self) -> str:
        if Path(self.path).is_file():
            return "file"
        else:
            return "dir"

    @computed_field
    @property
    def parent_dir(self) -> str:
        return f"{Path(self.path).parent}"

    @computed_field
    @property
    def created_at(self) -> str:
        _ctime: float = Path(self.path).stat().st_ctime
        ts: pendulum.DateTime = pendulum.from_timestamp(_ctime).to_iso8601_string()

        return ts

    @computed_field
    @property
    def modified_at(self) -> str:
        _mtime: float = Path(self.path).stat().st_mtime

        ts: pendulum.DateTime = pendulum.from_timestamp(_mtime).to_iso8601_string()

        return ts

    @computed_field
    @property
    def size_in_bytes(self) -> int | None:
        if Path(self.path).is_file():
            # If it's a file, directly get its size
            file_size_bytes = Path(self.path).stat().st_size
            return file_size_bytes
        elif Path(self.path).is_dir():
            # If it's a directory, recursively calculate total size
            total_size_bytes = 0
            for child in Path(self.path).iterdir():
                if child.is_file() and not child.is_symlink():
                    total_size_bytes += child.stat().st_size
            return total_size_bytes

        # try:
        #     return Path(self.path).stat().st_size
        # except Exception as exc:
        #     return None

    @computed_field
    @property
    def size_str(self) -> str | None:
        try:
            human_readable_str: str = converters.bytes_to_human_readable(
                size_in_bytes=self.size_in_bytes
            )

            return human_readable_str
        except Exception:
            return None

    @field_validator("path")
    def validate_path(cls, v) -> str:
        if isinstance(v, Path):
            return f"{v}"
        elif isinstance(v, str):
            return v
        else:
            raise TypeError(f"path must be of type str. Got type: ({type(v)})")


class ScanResults(BaseModel):
    """Object to store results of a directory path scan."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    scan_timestamp: str | None = Field(
        default=None,
        description="Time of scan. This value is None until a scan is run.",
    )
    scan_target: t.Union[str, Path] = Field(default=None)

    files: list[ScanEntity] = Field(default=None)
    dirs: list[ScanEntity] = Field(default=None)

    @computed_field
    @property
    def all(self) -> list[ScanEntity]:
        if self.files is None:
            self.files = []
        if self.dirs is None:
            self.dirs = []

        merged_list = []

        for f in self.dirs:
            if f not in merged_list:
                merged_list.append(f)
        for f in self.files:
            if f not in merged_list:
                merged_list.append(f)

        return merged_list

    @computed_field
    @property
    def count_dirs(self) -> int | None:
        if self.dirs is None:
            return 0
        else:
            return len(self.dirs)

    @computed_field
    @property
    def count_files(self) -> int | None:
        if self.files is None:
            return 0
        else:
            return len(self.files)

    @field_validator("scan_target")
    def validate_scan_target(cls, v) -> str:
        if isinstance(v, Path):
            return f"{v}"
        elif isinstance(v, str):
            return v
        else:
            raise TypeError(f"scan_target must be of type str. Got type: ({type(v)})")


class ScanTarget(BaseModel):
    """Manage scanning operations for a directory path.

    Params:
        path(typing.Union[str, Path]): A path to a directory to work with.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    path: t.Union[str, Path] = Field(default=None)

    @field_validator("path")
    def validate_path(cls, v) -> Path:
        assert v is not None, ValueError("@ScanTarget: path cannot be None")
        assert isinstance(v, str) or isinstance(v, Path), TypeError(
            f"@ScanTarget: path must be of type str or Path. Got type: {type(v)}"
        )
        if isinstance(v, str):
            v: Path = Path(v)

        return v

    @property
    def exists(self) -> bool:
        return self.path.exists()

    def get_files(
        self, as_str: bool = False
    ) -> list[ScanResults]:  # -> t.Union[list[str, os.DirEntry]]:
        """Return a list of file path strings found in self.path. Excludes directories.

        Params:
            as_str (bool): Control return list type.

        Returns:
            list[os.DirEntry]: If `as_str` = True`
            list[str]: (default) If `as_str = False`

        """
        return_files: list[t.Union[os.DirEntry, str]] = []
        _files: list[ScanEntity] = []

        if not self.exists:
            msg = FileNotFoundError(f"Could not find path '{self.path}'")
            print(f"[WARNING] {msg}")

            return None

        for entry in os.scandir(self.path):
            if entry.is_file():
                _files.append(ScanEntity(path=entry.path))

                if as_str:
                    return_files.append(entry.path)
                else:
                    return_files.append(entry)

        # self.files: list[ScanEntity] = _files

        return _files

    def get_dirs(
        self, as_str: bool = False
    ) -> list[ScanEntity]:  # -> t.Union[list[str, os.DirEntry]]:
        """Return a list of directory path strings found in self.path. Excludes directories.

        Params:
            as_str (bool): Control return list type.

        Returns:
            list[os.DirEntry]: If `as_str` = True`
            list[str]: (default) If `as_str = False`

        """
        return_dirs: list[t.Union[str, os.DirEntry]] = []
        _dirs: list[ScanEntity] = []

        for entry in os.scandir(self.path):
            if entry.is_dir():
                _dirs.append(ScanEntity(path=entry.path))
                if as_str:
                    return_dirs.append(entry.path)
                else:
                    return_dirs.append(entry)

        return _dirs

    def run_scan(self, as_str: bool = False) -> ScanResults:
        """Return a list of path strings found in self.path.

        Params:
            as_str (bool): Control return list type.

        Returns:
            list[os.DirEntry]: If `as_str` = True`
            list[str]: (default) If `as_str = False`

        """
        if not self.exists:
            msg = FileNotFoundError(f"Unable to find scan path: '{self.path}'")

            return None

        try:
            files: list[t.Union[str, os.DirEntry]] = self.get_files(as_str=as_str)
        except FileNotFoundError as fnf:
            msg = FileNotFoundError(f"Unable to find scan path: '{self.path}'")

            raise msg
        except Exception as exc:
            msg = Exception(f"Unhandled exception scanning for files. Details: {exc}")

            raise msg
        try:
            dirs: list[t.Union[str, os.DirEntry]] = self.get_dirs(as_str=as_str)
        except FileNotFoundError as fnf:
            msg = FileNotFoundError(f"Unable to find scan path: '{self.path}'")

            raise msg
        except Exception as exc:
            msg = Exception(f"Unhandled exception scanning for dirs. Details: {exc}")

            raise msg

        _results: ScanResults = ScanResults(
            scan_target=self.path, files=files, dirs=dirs
        )

        return _results


class Scanner(BaseModel):

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    scan_path: t.Union[str, Path] = Field(default=None)
    target: ScanTarget = Field(default=None)
    scan_results: ScanResults = Field(default=None)
    scan_timestamp: str | None = Field(
        default=None,
        description="Time of scan. This value is None until a scan is run.",
    )

    @field_validator("scan_path")
    def validate_path(cls, v) -> Path:
        assert v is not None, ValueError("@ScanTarget: path cannot be None")
        assert isinstance(v, str) or isinstance(v, Path), TypeError(
            f"@ScanTarget: path must be of type str or Path. Got type: {type(v)}"
        )
        if isinstance(v, str):
            v: Path = Path(v)

        return v

    @field_validator("scan_timestamp")
    def validate_timestamp(csl, v) -> str | None:
        if v is None:
            return None
        elif isinstance(v, pendulum.DateTime):
            return v.to_iso8601_string()
        elif isinstance(v, str):
            return v
        else:
            return None

    @property
    def count_objs(self) -> int:
        if not self.scan_path.exists():
            return None
        else:
            if self.scan_results.files is None:
                files: int = 0
            else:
                files: int = len(self.scan_results.files)

            if self.scan_results.dirs is None:
                dirs: int = 0
            else:
                dirs: int = len(self.scan_results.dirs)

            total: int = files + dirs

            return total

    def set_scan_timestamp(self) -> None:
        """Setter for self.scan_timestamp."""
        if self.scan_timestamp is None:
            _scan_ts: pendulum.DateTime = pendulum.now().to_iso8601_string()

            self.scan_timestamp = _scan_ts
        else:
            pass

    def scan(
        self,
        as_str: bool = False,
        save_results: bool = False,
        output_file: t.Union[str, Path] | None = None,
    ) -> ScanResults:
        self.target: ScanTarget = ScanTarget(path=self.scan_path)
        
        if PLATFORM.is_linux():
            print(f"Linux detected")
        elif PLATFORM.is_mac():
            print(f"Mac detected")
        elif PLATFORM.is_win():
            print(f"Windows detected")
        else:
            msg = Exception(f"Unable to detected OS type")
            print(f"[WARNING] {msg}")

        if not self.target.exists:
            msg = FileNotFoundError(f"Unable to find scan path: {self.target.path}'")

            print(f"[WARNING] {msg}")

            return None

        self.set_scan_timestamp()

        try:
            self.scan_results: ScanResults = self.target.run_scan(as_str=as_str)
        except FileNotFoundError as fnf:
            msg = FileNotFoundError(f"Unable to find scan path '{self.target.path}'")

            print(f"[ERROR] {msg}")
        except Exception as exc:
            msg = Exception(f"Unhandled exception scanning path '{self.target.path}'")
            print(f"[ERROR] {msg}")

        self.scan_results.scan_timestamp = self.scan_timestamp

        if save_results:
            assert output_file is not None, ValueError("output_file cannot be None")
            if isinstance(output_file, str):
                output_file: Path = Path(output_file)

            if not output_file.parent.exists():
                try:
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                except Exception as exc:
                    raise Exception(
                        f"Unhandled exception creating directory '{output_file.parent}'. Details: {exc}"
                    )

            try:
                self.save_to_json()
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception saving scan results to file '{output_file}'. Details: {exc}"
                )

                print(f"[ERROR] {msg}")

        return self.scan_results

    def save_to_json(
        self, output_file: t.Union[str, Path] | None = DEFAULT_SCAN_RESULTS_FILE
    ):
        """Save results object to JSON file."""
        assert output_file is not None, ValueError("output_file cannot be None")
        assert isinstance(output_file, str) or isinstance(output_file, Path), TypeError(
            f"output_file must be of type str or Path. Got type: {type(output_file)}"
        )

        if isinstance(output_file, str):
            output_file: Path = Path(output_file)

        try:
            data: str = json.dumps(self.scan_results.model_dump(), indent=2)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception dumping scan results to JSON. Details: {exc}"
            )
            print(f"[ERROR] {msg}")

            raise msg

        try:
            with open(output_file, "w") as f:
                f.write(data)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception writing scan results to file '{output_file}'. Details: {exc}"
            )
            print(f"[ERROR] {msg}")

            raise msg

    # def refresh_metadata(
    #     self, path_list: list[t.Union[str, os.DirEntry]] = True
    # ) -> list[os.DirEntry]:
    #     """Iterate of list of `os.DirEntry` objects, refreshing their metadata with `os.stat()`.

    #     Params:
    #         path_list (list[os.DirEntry]): List of `os.DirEntry` objects to iterate and refresh metadata.

    #     Returns:
    #         list[os.DirEntry]: The input list, with refreshed metadata.

    #     """
    #     assert path_list is not None, ValueError("path_list cannot be None")

    #     for p in path_list:
    #         try:
    #             os.stat(p)
    #         except Exception as exc:
    #             msg = Exception(
    #                 f"Unhandled exception refreshing file metadata with os.stat(). Details: {exc}"
    #             )
    #             print(f"[ERROR] {msg}")

    #     return path_list

from __future__ import annotations

import json
import os
from pathlib import Path
import typing as t

import uuid

import pendulum
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    computed_field,
    field_validator,
)


class ScanEntity(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    path: t.Union[str, Path] = Field(default=None)

    @computed_field
    @property
    def name(self) -> str:
        return f"{Path(self.path).name}"

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
    def created_at(self) -> pendulum.DateTime:
        _ctime: float = Path(self.path).stat().st_ctime
        ts: pendulum.DateTime = pendulum.from_timestamp(_ctime)

        return ts

    @computed_field
    @property
    def modified_at(self) -> pendulum.DateTime:
        _mtime: float = Path(self.path).stat().st_mtime

        ts: pendulum.DateTime = pendulum.from_timestamp(_mtime)

        return ts

    @computed_field
    @property
    def size(self) -> int | None:
        try:
            p = Path(self.path)
            if p.exists():
                creation_time = pendulum.from_timestamp(p.stat().st_ctime)
                modification_time = pendulum.from_timestamp(p.stat().st_mtime)
                return creation_time, modification_time
            else:
                return None, None
        except Exception as e:
            print(f"Error: {e}")
            return None, None

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

    scan_target: t.Union[str, Path] = Field(default=None)
    files: list[t.Union[str, os.DirEntry]] = Field(default=None)
    dirs: list[t.Union[str, os.DirEntry]] = Field(default=None)

    @property
    def count_dirs(self) -> int:
        return len(self.dirs)

    @property
    def count_files(self) -> int:
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
    scan_timestamp: t.Union[str, pendulum.DateTime] | None = Field(
        default=None,
        description="Time of scan. This value is None until a scan is run.",
    )

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

    @property
    def count_objs(self) -> int:
        if not self.exists:
            return None
        else:
            paths = self.get_paths()
            return len(paths)

    def set_scan_timestamp(self) -> None:
        """Called by other class methods to set the value of self.scan_timestamp."""
        if self.scan_timestamp is None:
            _scan_ts: pendulum.DateTime = pendulum.now()

            self.scan_timestamp = _scan_ts
        else:
            pass

    def refresh_metadata(
        self, path_list: list[t.Union[str, os.DirEntry]] = True
    ) -> list[os.DirEntry]:
        """Iterate of list of `os.DirEntry` objects, refreshing their metadata with `os.stat()`.

        Params:
            path_list (list[os.DirEntry]): List of `os.DirEntry` objects to iterate and refresh metadata.

        Returns:
            list[os.DirEntry]: The input list, with refreshed metadata.

        """
        assert path_list is not None, ValueError("path_list cannot be None")

        for p in path_list:
            try:
                os.stat(p)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception refreshing file metadata with os.stat(). Details: {exc}"
                )
                print(f"[ERROR] {msg}")

        return path_list

    def save_to_json(self, output_file: str = "scan_results/results.json") -> bool:
        """Output scan results to JSON file."""

        def prepare_results():
            all_paths: ScanResults = self.scan(as_str=True)

            json_obj: dict = {
                "target": f"{self.path}",
                "scan_timestamp": f"{self.scan_timestamp}",
                "count_total": self.count_objs,
                "count_dirs": len(all_paths.dirs),
                "count_files": len(all_paths.files),
                "scan_results": {"dirs": all_paths.dirs, "files": all_paths.files},
            }

            try:
                return_obj: str = json.dumps(json_obj, indent=2)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception creating JSON string of scan results. Details: {exc}"
                )

                raise msg

            return return_obj

        if not Path(output_file).parent.exists():
            try:
                Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception creating directory '{Path(output_file).parent}"
                )
                print(f"[ERROR] {msg}")

                return msg

        results_json: str = prepare_results()

        try:
            with open(output_file, "w") as f:
                f.write(results_json)

            return True
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception writing scan results to file '{output_file}'. Details: {exc}"
            )
            print(f"[ERROR] {msg}")

            return False

    def get_paths(self, as_str: bool = False) -> t.Union[list[os.DirEntry, str]]:
        """Return a list of path strings found in self.path.

        Params:
            as_str (bool): Control return list type.

        Returns:
            list[os.DirEntry]: If `as_str` = True`
            list[str]: (default) If `as_str = False`

        """
        paths: list[os.DirEntry] = []  # [i for i in os.scandir(SCAN_DIR.path)]

        self.set_scan_timestamp()

        for p in os.scandir(self.path):
            paths.append(p)

        if as_str:
            _paths: list[str] = []

            for p in paths:
                _path: str = p.path

                _paths.append(_path)

            return _paths
        else:
            return paths

    def get_files(self, as_str: bool = False) -> t.Union[list[str, os.DirEntry]]:
        """Return a list of file path strings found in self.path. Excludes directories.

        Params:
            as_str (bool): Control return list type.

        Returns:
            list[os.DirEntry]: If `as_str` = True`
            list[str]: (default) If `as_str = False`

        """
        _files: list[t.Union[os.DirEntry, str]] = []

        self.set_scan_timestamp()

        for entry in os.scandir(self.path):
            if entry.is_file():
                if as_str:
                    _files.append(entry.path)
                else:
                    _files.append(entry)

        return _files

    def get_dirs(self, as_str: bool = False) -> t.Union[list[str, os.DirEntry]]:
        """Return a list of directory path strings found in self.path. Excludes directories.

        Params:
            as_str (bool): Control return list type.

        Returns:
            list[os.DirEntry]: If `as_str` = True`
            list[str]: (default) If `as_str = False`

        """
        _dirs: list[t.Union[Path, os.DirEntry]] = []

        self.set_scan_timestamp()

        for entry in os.scandir(self.path):
            if entry.is_dir():
                if as_str:
                    _dirs.append(entry.path)
                else:
                    _dirs.append(entry)

        return _dirs

    def get_files_dirs(self, as_str: bool = False) -> ScanResults:
        """Return a list of path strings found in self.path.

        Params:
            as_str (bool): Control return list type.

        Returns:
            list[os.DirEntry]: If `as_str` = True`
            list[str]: (default) If `as_str = False`

        """
        files: list[t.Union[str, os.DirEntry]] = self.get_files(as_str=as_str)
        dirs: list[t.Union[str, os.DirEntry]] = self.get_dirs(as_str=as_str)

        # return {"dirs": dirs, "files": files}
        return ScanResults(scan_target=self.path, files=files, dirs=dirs)

    def get_pathlib_paths(self) -> list[Path]:
        """Return list of files as `pathlib.Path` objects."""
        paths: list[Path] = []

        for f in self.get_paths(as_str=True):
            paths.append(Path(f))

        return paths

    def scan(
        self,
        as_str: bool = False,
        save: bool = True,
        output_file: t.Union[str, Path] | None = None,
    ) -> ScanResults:
        results: ScanResults = self.get_files_dirs(as_str=as_str)

        if save:
            if output_file is None:
                output_file: str = "red_fileops-scan_results.json"
            else:
                if isinstance(output_file, Path):
                    output_file: str = f"{output_file}"

            self.save_to_json(output_file=output_file)

        return results


class Scanner(BaseModel):

    path: t.Union[str, Path] = Field(default=None)
    target: ScanTarget = Field(default=None)
    scan_results: ScanResults = Field(default=None)

    @field_validator("path")
    def validate_path(cls, v) -> Path:
        assert v is not None, ValueError("@ScanTarget: path cannot be None")
        assert isinstance(v, str) or isinstance(v, Path), TypeError(
            f"@ScanTarget: path must be of type str or Path. Got type: {type(v)}"
        )
        if isinstance(v, str):
            v: Path = Path(v)

        return v

    def scan(self):
        self.target: ScanTarget = ScanTarget(path=self.path)
        self.scan_results: ScanResults = self.target.scan()

        self.target.save_to_json()

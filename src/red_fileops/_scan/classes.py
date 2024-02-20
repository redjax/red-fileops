import os
import json
from pathlib import Path
import typing as t
import pendulum

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    ValidationError,
    ConfigDict,
    computed_field,
)


class ScanResults(BaseModel):
    """Object to store results of a directory path scan."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    scan_target: t.Union[str, Path] = Field(default=None)
    files: list[t.Union[str, os.DirEntry]] = Field(default=None)
    dirs: list[t.Union[str, os.DirEntry]] = Field(default=None)

    @field_validator("scan_target")
    def validate_scan_target(cls, v) -> str:
        if isinstance(v, Path):
            return f"{v}"
        elif isinstance(v, str):
            return v
        else:
            raise TypeError(f"scan_target must be of type str. Got type: ({type(v)})")


class ScanDir(BaseModel):
    """Manage scanning operations for a directory path.

    Params:
        path(typing.Union[str, Path]): A path to a directory to work with.
    """

    path: t.Union[str, Path] = Field(default=None)

    @field_validator("path")
    def validate_path(cls, v) -> Path:
        assert v is not None, ValueError("@ScanDir: path cannot be None")
        assert isinstance(v, str) or isinstance(v, Path), TypeError(
            f"@ScanDir: path must be of type str or Path. Got type: {type(v)}"
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

    def to_json(self, output_file: str = "scan_results/results.json") -> bool:
        """Output scan results to JSON file."""
        if not Path(output_file).parent.exists():
            try:
                Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception creating directory '{Path(output_file).parent}"
                )
                print(f"[ERROR] {msg}")

                return msg

        try:
            with open(output_file, "w") as f:
                data = json.dumps(self.get_dirs_files(as_str=True).__dict__)
                f.write(data)

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

        for entry in os.scandir(self.path):
            if entry.is_dir():
                pass
            else:
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

        for entry in os.scandir(self.path):
            if entry.is_dir():
                pass
            else:
                if as_str:
                    _dirs.append(entry.path)
                else:
                    _dirs.append(entry)

        return _dirs

    def get_dirs_files(
        self, as_str: bool = False
    ) -> dict[str, list[t.Union[str, os.DirEntry]]]:
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

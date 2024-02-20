from __future__ import annotations

from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import typing as t

from red_fileops.scan import ScanResults, ScanTarget

import pendulum

if __name__ == "__main__":
    SCAN_DIR: ScanTarget = ScanTarget(path=Path("D:/Data/Downloads/"))

    if not SCAN_DIR.exists:
        raise FileNotFoundError(f"Could not find path: {SCAN_DIR.path}")

    paths: list[t.Union[str, os.DirEntry]] = SCAN_DIR.get_paths(as_str=False)

    print(f"Found [{SCAN_DIR.count_objs}] path(s) in '{SCAN_DIR}'")

    # # print(f"Files & dirs: {SCAN_DIR.get_files(as_paths=True)}")

    SCAN_DIR.refresh_metadata(path_list=paths)
    test = SCAN_DIR.get_files(as_str=False)[0]
    print(f"Test file ({test}): {test}")

    test_pathlib = SCAN_DIR.get_pathlib_paths()[0]
    print(f"Example pathlib Path ({type(test_pathlib)}): {test_pathlib}")

    # SCAN_DIR.to_json(
    #     output_file=f"scan_results/{pendulum.now().format('YYYY-MM-DD_HH-mm-ss')}_results.json"
    # )
    SCAN_DIR.save_to_json()

    SCAN_DIR.refresh_metadata(path_list=["./scan_results/results.json"])

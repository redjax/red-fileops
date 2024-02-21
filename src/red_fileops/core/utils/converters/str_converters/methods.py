from __future__ import annotations

def bytes_to_human_readable(size_in_bytes: int = None) -> str:
    """Return a human-readable string from an input integer size in bytes.

    Examples:
        - input: `1025`
        - output: "`1 GB`"
    
    """
    if size_in_bytes is None:
        return "0 bytes"

    assert isinstance(size_in_bytes, int), TypeError(
        f"size_in_bytes must be of type int. Got type: ({type(size_in_bytes)})."
    )
    assert size_in_bytes >= 0, ValueError(
        f"size_in_bytes should be a positive integer. Got value: {size_in_bytes}"
    )

    suffixes = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    i = 0

    while size_in_bytes >= 1024 and i < len(suffixes) - 1:
        size_in_bytes /= 1024
        i += 1

    formatted_size = f"{size_in_bytes:.1f} {suffixes[i]}"
    return formatted_size

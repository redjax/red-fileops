from __future__ import annotations

from .schemas import PlatformInfo

def print_platform(p: PlatformInfo = None, print_large_values: bool = False) -> None:
    """Print report on platform.

    Params:
    -------

    p (PlatformInfo): Instance of PlatformInfo class. Diagnostic strings will be created from p's properties.

    print_large_values (bool): When True, large lists (like p.python.modules) will be printed.
    """
    ## Compose multiline string for platform debug message
    platform_msg: str = f"""
--- [ Platform Info ]

    System: {p.system}
    Platform: {p.platform}
    Release: {p.release}
    Version: {p.version}
    Machine: {p.machine}
    Architecture: {p.arch}
"""

    ## Compose multiline string for uname debug message
    uname_msg: str = f"""
--- [ Uname ]

    Node (network name): {p.uname.node}
    System: {p.uname.system}
    Release: {p.uname.release}
    OS Version: {p.uname.version}
    Machine: {p.uname.machine}
"""

    ## Compose multiline string for Python message
    python_msg: str = f"""
--- [ Python Diagnostics ]

    Version: {p.python.version}
    Build: {p.python.build}
    Compiler: {p.python.compiler}
    Implementation: {p.python.implementation}
    
    env:PYTHONDONTWRITEBYTECODE = {p.python.dont_write_bytecode}
        - note: when False, .pyc files will be created. To disable .pyc caching,
          set PYTHONDONTWRITEBYTECODE environment variable to True.
    
    CLI Flags: {p.python.flags}
    
    Python Base Prefix: {p.python.exec_prefix}
    Python Executable: {p.python.executable}
"""

    ## If print_large_values is True, append p.python values with large outputs
    if print_large_values:
        python_msg = (
            python_msg
            + f"""    
    Python PATH:\n{p.python.path}

    Loaded Modules:\n{p.python.modules}
"""
        )

    ## Initialize list of messages to loop over & print
    print_msgs = [platform_msg, uname_msg, python_msg]

    ## Print composed messages
    for msg in print_msgs:
        print(msg)

import ctypes
import os


def get_sid():
    user = os.getlogin()
    domain = os.environ["USERDOMAIN"]
    token = ctypes.windll.advapi32.OpenProcessToken(-1, 0x02000000, 0)
    user_sid = ctypes.create_string_buffer(1024)
    user_sid_size = ctypes.c_ulong(ctypes.sizeof(user_sid))
    domain_name = ctypes.create_string_buffer(1024)
    domain_name_size = ctypes.c_ulong(ctypes.sizeof(domain_name))
    sid_name_use = ctypes.c_ulong()
    ctypes.windll.advapi32.LookupAccountNameW(
        None,
        user,
        user_sid,
        ctypes.byref(user_sid_size),
        domain_name,
        ctypes.byref(domain_name_size),
        ctypes.byref(sid_name_use),
    )
    return user_sid.value.decode("utf-8")


def get_groups():
    raise NotImplementedError("Function get user's groups is not supported on Windows.")

    user = os.getlogin()
    domain = os.environ["USERDOMAIN"]
    token = ctypes.windll.advapi32.OpenProcessToken(-1, 0x02000000, 0)
    user_sid = ctypes.create_string_buffer(1024)
    user_sid_size = ctypes.c_ulong(ctypes.sizeof(user_sid))
    domain_name = ctypes.create_string_buffer(1024)
    domain_name_size = ctypes.c_ulong(ctypes.sizeof(domain_name))
    sid_name_use = ctypes.c_ulong()
    ctypes.windll.advapi32.LookupAccountNameW(
        None,
        user,
        user_sid,
        ctypes.byref(user_sid_size),
        domain_name,
        ctypes.byref(domain_name_size),
        ctypes.byref(sid_name_use),
    )
    groups = []
    for group in ctypes.windll.advapi32.GetTokenInformation(
        token, 2, None, 0, ctypes.byref(ctypes.c_ulong())
    ):
        group_name = ctypes.create_string_buffer(1024)
        group_name_size = ctypes.c_ulong(ctypes.sizeof(group_name))
        ctypes.windll.advapi32.LookupAccountSidW(
            None,
            group,
            group_name,
            ctypes.byref(group_name_size),
            domain_name,
            ctypes.byref(domain_name_size),
            ctypes.byref(sid_name_use),
        )
        groups.append(group_name.value.decode("utf-8"))
    return groups

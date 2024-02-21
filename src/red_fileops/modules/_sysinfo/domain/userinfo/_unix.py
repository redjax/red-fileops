import pwd
import os
import subprocess


def get_uuid():
    try:
        return pwd.getpwnam(os.getlogin()).pw_uid
    except Exception as exc:
        raise Exception(
            f"Unix OS type detected, but could not get current user's UID. Details: {exc}"
        )


def get_groups():
    output = subprocess.check_output(["id", "-Gn", os.getlogin()])
    return output.decode("utf-8").strip().split(" ")

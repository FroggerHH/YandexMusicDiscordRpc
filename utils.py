import os

debug_mode = False


def execute(cmd: str) -> str:
    output = os.popen(cmd)
    out = output.read().removesuffix('\n')
    if debug_mode:
        print(">>" + out)
    return out


def format_time(milliseconds):
    total_seconds = milliseconds // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


def ms_to_sec(ms):
    return ms // 1000

# Nagios exit codes:
OK = 0
WARN = 1
CRIT = 2
UNKNOWN = 3


def status_code_to_label(code):
    return {
        OK: "OK",
        WARN: "WARN",
        CRIT: "CRIT",
        UNKNOWN: "UNKNOWN"
    }.get(code, "UNKNOWN")

#!/usr/bin/env python
import re
import sys
from subprocess import CalledProcessError

from openshift import oc
import nagios


check_disk_cmd = ("df", "--output=target,pcent,ipcent")
# Example output:
# /etc/hosts      19%    8%
check_disk_output_pattern = re.compile(r"([\w/]+)\s+(\d+)%\s+(\d+)%")


def parse_df(line):
    mo = check_disk_output_pattern.match(line)
    if mo is None:
        return ()
    return (mo.group(1), int(mo.group(2)), int(mo.group(3)))


def analize(pcent, ipcent, warning_threshold, critical_threshold):
    max_pcent = max(pcent, ipcent)
    return max_pcent >= warning_threshold, max_pcent >= critical_threshold


def report():
    raise NotImplementedError("report is not implemented yet")


def main():
    project = oc("project", "-q")
    print analize(map(parse_df, exec_in_pods(project, get_running_pod_names(), check_disk_cmd)))


if __name__ == "__main__":
    try:
        main()
    except CalledProcessError:
        pass
    except KeyError:
        pass
    except:
        sys.exit(nagios.UNKNOWN)

# TODO: check that critical threshold is always >= warning threshold
# TODO: what if nothing is checked? (empty output from df, etc)

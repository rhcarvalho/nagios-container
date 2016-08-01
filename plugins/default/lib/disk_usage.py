#!/usr/bin/env python
import argparse
import re
import sys
import traceback
from collections import Counter

import openshift
import nagios


def generate_parser():
    parser = argparse.ArgumentParser(
        description="Checks the disk usage (blocks and inodes)",
    )
    parser.add_argument(
        "-w", "--warn", type=int, required=True,
        help="set warning threshold of disk usage (%% of blocks or inodes)",
    )
    parser.add_argument(
        "-c", "--crit", type=int, required=True,
        help="set critical threshold of disk usage (%% of blocks or inodes), "
             "must be higher than or equal the warning threshold",
    )
    return parser


check_disk_cmd = ("df", "--output=pcent,ipcent,target")
# Example output:
# Use% IUse% Mounted on
#   1%    1% /
#  20%    8% /etc/hosts
check_disk_output_pattern = re.compile(r"\s*(\d+)%\s+(\d+)%\s+(.+)$")


def parse_df_line(line):
    mo = check_disk_output_pattern.match(line)
    if mo is None:
        return ()
    return mo.group(3), int(mo.group(1)), int(mo.group(2))


def parse_df_lines(lines):
    return filter(None, map(parse_df_line, lines.splitlines()))


def analize(pod, disks, warning_threshold, critical_threshold):
    results = []
    for mount, space_usage, inode_usage in disks:
        max_pcent = max(space_usage, inode_usage)

        disk_status = nagios.UNKNOWN
        if max_pcent >= critical_threshold:
            disk_status = nagios.CRIT
        elif max_pcent >= warning_threshold:
            disk_status = nagios.WARN
        elif max_pcent < warning_threshold:
            disk_status = nagios.OK

        results.append([pod, mount, space_usage, inode_usage, disk_status])
    return results


def report(results):
    # REVIEW: is nagios.UNKNOWN the best here?
    if not results:
        return nagios.UNKNOWN

    unique_statuses = Counter(
        disk_status
        for pod, mount, space_usage, inode_usage, disk_status in results
    )

    ret = max(unique_statuses)

    if ret == nagios.OK:
        print "%s: All %s volumes are under the warning threshold" % (
            nagios.status_code_to_label(ret), len(results))
    elif ret == nagios.UNKNOWN:
        print "%s: Unable to determine usage on %s volumes" % (
            nagios.status_code_to_label(ret), unique_statuses[nagios.UNKNOWN])
    elif ret == nagios.WARN:
        print "%s: There are %s volumes over the warning threshold" % (
            nagios.status_code_to_label(ret), unique_statuses[nagios.WARN])
    else:
        print "%s: There are %s volumes over the critical threshold and %s volumes over the warning threshold" % (
            nagios.status_code_to_label(ret), unique_statuses[nagios.CRIT], unique_statuses[nagios.WARN])

    for pod, mount, disk_usage, inode_usage, status in results:
        print "%s: %s:%s - bytes used: %s%%, inodes used: %s%%" % (
            nagios.status_code_to_label(status), pod, mount, disk_usage, inode_usage)

    return ret


def check(warn, crit):
    if crit < warn:
        msg = "critical threshold cannot be lower than warning threshold: %d < %d"
        raise ValueError(msg % (crit, warn))

    project = openshift.get_project()

    results = []

    pods = openshift.get_running_pod_names(project)
    execs = openshift.exec_in_pods(project, pods, check_disk_cmd)
    for pod, lines in zip(pods, execs):
        results.extend(analize(pod, parse_df_lines(lines), warn, crit))

    return report(results)


if __name__ == "__main__":
    args = generate_parser().parse_args()
    code = nagios.UNKNOWN
    try:
        code = check(args.warn, args.crit)
    except:
        traceback.print_exc()
    finally:
        sys.exit(code)

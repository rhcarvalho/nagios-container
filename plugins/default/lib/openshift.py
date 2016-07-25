import json
from subprocess import check_output


def oc(*args):
    return check_output(("oc",) + args)


def _get_running_pod_names(oc, project):
    # Manually filter Running pods because of a bug in `oc get`, see:
    # https://github.com/kubernetes/kubernetes/issues/29115
    # return oc("-n", project, "get", "pods", "--show-all=false", "-o", "name")
    pods = json.loads(oc("-n", project, "get", "pods", "--show-all=false", "-o", "json"))
    return [p["metadata"]["name"] for p in pods if p["status"]["phase"] == "Running"]


def get_running_pod_names(project):
    return _get_running_pods(oc, project)


def _exec_in_pods(oc, project, pods, cmd):
    return [oc("-n", project, "exec", name, "--", *cmd) for name in pods]


def exec_in_pods(project, pods, cmd):
    return _exec_in_all_runnning_pods(oc, project, pods, cmd)

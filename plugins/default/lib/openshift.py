import json
from subprocess import check_output


def oc(*args):
    return check_output(("oc",) + args)


def _get_service_selectors(oc, project, service):
    svc = json.loads(oc("-n", project, "get", "service", service, "-o", "json"))
    return [k + "=" + v for k, v in svc["spec"]["selector"].items()]


def get_service_selectors(project, service):
    return _get_service_selectors(oc, project, service)


def _get_running_pod_names(oc, project, selector=None, container_names=None):
    # Manually filter Running pods because of a bug in `oc get`, see:
    # https://github.com/kubernetes/kubernetes/issues/29115
    # return oc("-n", project, "get", "pods", "--show-all=false", "-o", "name")
    args = ("-n", project, "get", "pods", "--show-all=false", "-o", "json")

    if selector:
        args += ("--selector=" + ",".join(selector),)

    pods = json.loads(oc(*args))["items"]

    if container_names:
        pods = [p for p in pods for c in p["spec"]["containers"] if c["name"] in container_names]

    return [p["metadata"]["name"] for p in pods if p["status"]["phase"] == "Running"]


def get_running_pod_names(project, selector=None, container_names=None):
    return _get_running_pod_names(oc, project, selector, container_names)


def _exec_in_pods(oc, project, pods, cmd):
    return [oc("-n", project, "exec", name, "--", *cmd) for name in pods]


def exec_in_pods(project, pods, cmd):
    return _exec_in_pods(oc, project, pods, cmd)


def get_project():
    with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace") as f:
        data = f.read().rstrip("\n")
    return data

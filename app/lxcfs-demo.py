#!/usr/bin/env python
# Time: 2020.8.1
# BY:The Last Name

from flask import Flask, request, jsonify
from pprint import pprint
import base64
import copy
import json
import jsonpatch
import os
import re

app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():

    allowed = True
    request_info = json.loads(request.get_data(as_text=True))

    modified_spec = copy.deepcopy(request_info)
    uid = modified_spec["request"]["uid"]
    workload_metadata = modified_spec["request"]["object"]["metadata"]
    workload_type = modified_spec["request"]["kind"]["kind"]
    namespace = modified_spec["request"]["namespace"]

    print("")
    print("##################################################################")
    print("")

    # Detect if "name" in object metadata
    # this was added because the request object for pods don't 
    # include a "name" field in the object metadata. This is because generateName
    # occurs Server Side post-admission
    if "name" in workload_metadata:
        workload = modified_spec["request"]["object"]["metadata"]["name"]
    elif "generateName" in workload_metadata:
        workload = modified_spec["request"]["object"]["metadata"]["generateName"]
    else:
        workload = uid

    # Change workflow/json path based on K8s object type
    if workload_type == "Pod":
        append_volumeMounts(modified_spec["request"]["object"]["spec"]["containers"][0])
        append_volumes(modified_spec["request"]["object"]["spec"])
    else:
        append_volumeMounts(modified_spec["request"]["object"]["spec"]["template"]["spec"]["containers"][0])
        append_volumes(modified_spec["request"]["object"]["spec"]["template"]["spec"])

    print("[INFO] - Diffing original request to modified request and generating JSONPatch")
    patch = jsonpatch.JsonPatch.from_diff(request_info["request"]["object"], modified_spec["request"]["object"])

    print("[INFO] - JSON Patch: {}".format(patch))
    admission_response = {
        "allowed": True,
        "uid": request_info["request"]["uid"],
        "patch": base64.b64encode(str(patch).encode()).decode(),
        "patchtype": "JSONPatch"
    }
    admissionReview = {
        "response": admission_response
    }

    print("[INFO] - Sending Response to K8s API Server:")
    pprint(admissionReview)
    pprint(modified_spec)
    return jsonify(admissionReview)

def append_volumes(container_spec):
    pprint(container_spec)
    volumes_tem=[{"name": "lxcfs-cpuinfo","hostPath": {"path": "/var/lib/lxcfs/proc/cpuinfo"}},
                 {"name": "lxcfs-diskstats","hostPath": {"path": "/var/lib/lxcfs/proc/diskstats"}},
                 {"name": "lxcfs-meminfo","hostPath": {"path": "/var/lib/lxcfs/proc/meminfo"}},
                 {"name": "lxcfs-stat","hostPath": {"path": "/var/lib/lxcfs/proc/stat"}},
                 {"name": "lxcfs-swaps","hostPath": {"path": "/var/lib/lxcfs/proc/swaps"}},
                 {"name": "lxcfs-uptime","hostPath": {"path": "/var/lib/lxcfs/proc/uptime"}}]
    if "volumes" in container_spec:
        container_spec["volumes"] = container_spec["volumes"] + volumes_tem
    else:
        container_spec["volumes"] = volumes_tem

def append_volumeMounts(container_spec):
    pprint(container_spec)
    volumeMounts_tem=[{"mountPath": "/proc/cpuinfo","name": "lxcfs-cpuinfo"},
                {"mountPath": "/proc/diskstats","name": "lxcfs-diskstats"},
                {"mountPath": "/proc/meminfo","name": "lxcfs-meminfo"},
                {"mountPath": "/proc/stat","name": "lxcfs-stat"},
                {"mountPath": "/proc/swaps","name": "lxcfs-swaps"},
                {"mountPath": "/proc/uptime","name": "lxcfs-uptime"}]
    if "volumeMounts" in container_spec:
        container_spec["volumeMounts"] = container_spec["volumeMounts"] + volumeMounts_tem
    else:
        container_spec["volumeMounts"] = volumeMounts_tem


#app.run(host='0.0.0.0', port=5000, debug=True)
app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('./ssl/cert.pem', './ssl/key.pem'))


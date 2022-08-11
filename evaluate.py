# Sample JSON piped from metric.py to evaluate.py
# {
#   "resource": "testcpa",
#   "runType": "api",
#   "metrics": [
#     {
#       "resource": "testcpa",
#       "value": "{\"current_replicas\": 4, \"avgcpu_utilization\": 75}"
#     }
#   ]
# }

import json
import sys
import math

def main():
    #Turn JSON into a python dictionary
    spec = json.loads(sys.stdin.read())
    evaluate(spec)

def evaluate(spec):
    # Only expect 1 metric provided
    if len(spec["metrics"]) != 1:
        sys.stderr.write("Expected 1 metric")
        exit(1)

    # Retrieve metric value, there should only be 1
    eval_metric = json.loads(spec["metrics"][0]["value"])

    # Retrieve current replicas from metrics piped
    current_replicas = eval_metric["current_replicas"]
    # Retrieve average utilization from metrics
    avgcpu_utilization = eval_metric["avgcpu_utilization"]
    
    #Main logic for evaluator to calculate the number of replicas based on utilisation - Same logic can be used for any metric
    target_replicas = current_replicas
    if ((avgcpu_utilization > 50) and (avgcpu_utilization <= 100)):
        target_replicas += 1
    if ((avgcpu_utilization > 100) and (avgcpu_utilization <= 140)):
        target_replicas += 2
    if ((avgcpu_utilization > 140) and (avgcpu_utilization <= 180)):
        target_replicas += 3
    if (avgcpu_utilization > 180):
        target_replicas += 4
    else:
        target_replicas = math.ceil((target_replicas*(avgcpu_utilization/50)))
    # Build JSON to pass to CPA for scaling
    evaluation = {}
    evaluation["targetReplicas"] = target_replicas

    # Output JSON to stdout
    sys.stdout.write(json.dumps(evaluation))

if __name__ == "__main__":
    main()
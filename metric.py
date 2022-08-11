# Sample JSON piped into the metric.py
# { ##FOR CPU
#   "resource": {...},
#   "runType": "scaler",
#   "kubernetesMetrics": [
#     {
#       "current_replicas": 1,
#       "spec": {
#         "type": "Resource",
#         "resource": {
#           "name": "cpu",
#           "target": {
#             "type": "Utilization"
#           }
#         }
#       },
#       "resource": {
#         "pod_metrics_info": {
#           "flask-metric-697794dd85-bsttm": {
#             "Timestamp": "2021-04-05T18:10:10Z",
#             "Window": 30000000000,
#             "Value": 4
#           }
#         },
# { ##FOR PACKETS-PER-SECOND 
#   "resource": {...},
#   "runType": "scaler",
#   "kubernetesMetrics": [
#     {
#       "current_replicas": 1,
#       "spec": {
#         "type": "Pods",
#         "pods": {
#           "metric": {
#             "name": "packets-per-second",
#           },
#           "target": {
#             "type": "AverageValue"
#           }
#         }
#       },
#       "resource": {
#         "pod_metrics_info": {
#           "flask-metric-697794dd85-bsttm": {
#             "Timestamp": "2021-04-05T18:10:10Z",
#             "Window": 30000000000,
#             "Value": 1000
#           }
# { ##FOR CUSTOM METRICS
#   "resource": {...},
#   "runType": "scaler",
#   "kubernetesMetrics": [
#     {
#       "current_replicas": 1,
#       "spec": {
#         "type": "External",
#         "metric": {
#           "name": "queue_messages_ready",
#           "selector": "queue=worker_tasks",
#           "target": {
#             "type": "AverageValue"
#           }
#         }
#       },
#       "external": {
#         "current": {
#           "average_value": 5
#         },
#         "ready_pod_count": 1,
#         "timestamp": "2021-04-05T18:10:10Z"
#       }
#     }
#   ]
# }


import json
import sys

def main():
    #Turn JSON into a python dictionary
    spec = json.loads(sys.stdin.read())
    metric(spec)

def metric(spec):
    cpu_utilization = 0
    #Kubernetes metrics is taken from the pipeline -- Refer to JSON piped above
    metrics = spec["kubernetesMetrics"][0]

    #Current replicas now running are evaluated from the Kubernetes metrics
    current_replicas = metrics["current_replicas"]
    
    #CPU metrics are taken for the entire cluster and the per pod metrocs are taken from this
    cpu_stats = metrics["resource"]
    perpod_metrics = cpu_stats["pod_metrics_info"]
    
    #Get total utilisation value from all pods
    for _, pod_info in perpod_metrics.items():
        cpu_utilization += pod_info["Value"]
    # Calculate the average utilization
    avgcpu_utilization = cpu_utilization / current_replicas
    #JSON generated for sendng it to Evaluate.py
    sys.stdout.write(json.dumps(
        {
            "current_replicas": current_replicas,
            "avgcpu_utilization": avgcpu_utilization
        }
    ))

if __name__ == "__main__":
    main()

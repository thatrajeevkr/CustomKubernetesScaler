# Custom Pod Autoscaler 

This project is created as a part of University project. Not to be used externally

This follows step by step guide to implement the scaler into our Kubernetes system

### Prerrequisites:
    Kubernetes cluster installed
    Docker installed
    metricserver configured
    Promethues community (optional)

### Installing
Clone the [CustomKubernetesScaler](https://github.com/thatrajeevkr/CustomKubernetesScaler) repository:
```bash
git clone https://github.com/thatrajeevkr/CustomKubernetesScaler
cd CustomKubernetesScaler
```

Deploy custom scaling operator, config file, metric file, evaluate file, cpa file and Deployment file

```bash
VERSION=v1.1.0
kubectl apply -f https://github.com/jthomperoo/custom-pod-autoscaler-operator/releases/download/${VERSION}/cluster.yaml

kubectl apply -f deployment.yaml

docker build -t CustomKubernetesScaler .

kubectl apply -f cpa.yaml
```

After waiting for a couple of seconds, we can see that the scaler and deployment are successfully running.
If changes needed to be done to add any other deployment already present, we have to modify cpa.yaml and change the deployment file.
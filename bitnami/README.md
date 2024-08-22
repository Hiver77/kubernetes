# Spark Running on Kubernetes using Helm Charts!!!

This is a repo containing the necessary things to get you up and running with spark, helm and kubernetes

## Prerequisites

- Have docker desktop for mac installed [here](https://docs.docker.com/desktop/install/mac-install/).
- Enable the Kubernetes cluster within docker desktop [here](https://docs.docker.com/desktop/kubernetes/).
- Have Kubetctl [here] (https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/)
- Install helm with brew following instructions [here](https://docs.docker.com/desktop/install/mac-install/).


## Now to get it installed

1. Install the chart:

```console
### Add bitnami repo to your own repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install spark-release bitnami/spark --set worker.replicaCount=1 --namespace spark --create-namespace

### uninstall all pods for release name:
helm ls -n spark
helm uninstall spark-release -n spark

### Check if kubernetes is running
kubectl get nodes -n spark
```

2. Run spark-pi example:
This code is an example of how to calculate the approximate value of Pi using a Monte Carlo method. 
Inputs: number of partitions which data will be separeted and it works to calculate number of samples

How Can I get spark master url?
kubectl get svc -n spark
spark-release-master-svc:7077

Run this command in your terminal
kubectl exec -ti -n spark spark-release-master-0 -- spark-submit --master spark://spark-release-master-svc:7077 \
  --conf spark.kubernetes.container.image=bitnami/spark:3 \
  --class org.apache.spark.examples.SparkPi \
  /opt/bitnami/spark/examples/jars/spark-examples_2.12-3.5.1.jar 50

kubectl exec -ti -n spark spark-release-master-0 -- spark-submit --master spark://spark-release-master-svc:7077 \
  --conf spark.kubernetes.container.image=bitnami/spark:3 \
  --class org.apache.spark.examples.SparkPi \
  /opt/bitnami/spark/examples/src/main/python/pi.py 50


3. enable Kubernetes dashboard
```console
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard
```
3.1 create Creating sample user
We are going to crea a new servicesAccount with cluster-admin permissions
```console
kubectl apply -f dashboard-adminuser.yaml
```

3.2 Open Kubernetes dashboard
```console
 kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443
```

3.3 Generate a new token
```console
kubectl -n kubernetes-dashboard create token admin-user
```
Go to URL: 127.0.0.1:8443

3.4 clean up
```console
kubectl -n kubernetes-dashboard delete serviceaccount admin-user
kubectl -n kubernetes-dashboard delete clusterrolebinding admin-user
```
4. enable Spark UI
kubectl port-forward --namespace spark svc/spark-release-master-svc 8081:80

go to URL: 127.0.0.1:8081

5. Run your own project
kubectl cp pysparkexample.py spark-release-master-0:/opt/bitnami/spark/tmp -n spark

kubectl exec -ti -n spark spark-release-master-0 -- spark-submit --master spark://spark-release-master-svc:7077 /opt/bitnami/spark/tmp/pysparkexample.py

6. enable interactive pyspark shell 
6.1 copy new pyspark bash script
kubectl cp pyspark spark-release-master-0:/opt/bitnami/spark/pyspark_shell -n spark
6.2 Move to new location opt/bitnami/spark/pyspark_shell and run
./pyspark
6.3 run pysparkexample_

# Spark Running on Kubernetes using Helm Charts!!!

This is a repo containing the necessary things to get you up and running with spark, helm and kubernetes

## Prerequisites

- Have docker desktop for mac installed [here](https://docs.docker.com/desktop/install/mac-install/).
- Enable the Kubernetes cluster within docker desktop [here](https://docs.docker.com/desktop/kubernetes/).
- Install helm with brew following instructions [here](https://docs.docker.com/desktop/install/mac-install/).

## Now to get it installed

1. Install the chart:

```console
### Add bitnami repo to your own repository
helm install spark-kuberney spark-operator/spark-operator --namespace spark-kuberney --create-namespace --set webhook.enable=true
```

2. Modify the pyspark script **pysparkexample.py** , add your own code and save the changes.

3. Build the Docker Image and push it to a registry, in this case I'm using my own registry:

```console
docker build -t spark-custom .
docker tag spark-custom {YOUR-DOCKER-REPO}:spark-custom 
docker push {YOUR-DOCKER-REPO}:spark-custom             
```

4. Modify the SparkApplication yaml to submit and reference the application and the file

5. Deploy the file

```console
kubectl delete sparkapplication spark-custom-example -n spark-kuberney
kubectl apply -f pyspark-application.yaml -n spark-kuberney
kubectl logs spark-custom-example-driver -n spark-kuberney -f
```
6. Check the application pods and the logs

```console
kubectl get pods -n spark-operator
kubectl logs spark-custom-example-driver -n spark-operator
```

```console
kubectl describe pod spark-custom-example-driver -n spark-operator
```
6. Delete the application

kubectl delete sparkapplication spark-custom-example -n spark-operator

# Running an independent pod with the console

kubectl run -it --rm pyspark-console --image={YOUR-DOCKER-REPO}:spark-custom -- bash

7. enable Kubernetes dashboard
```console
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard
```
7.1 create Creating sample user
We are going to crea a new servicesAccount with cluster-admin permissions
```console
kubectl apply -f dashboard-adminuser.yaml
```

7.2 Open Kubernetes dashboard
```console
 kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443
```

7.3 Generate a new token
```console
kubectl -n kubernetes-dashboard create token admin-user
```
Go to URL: 127.0.0.1:8443

7.4 clean up
```console
kubectl -n kubernetes-dashboard delete serviceaccount admin-user
kubectl -n kubernetes-dashboard delete clusterrolebinding admin-user
```
8. enable Spark UI
kubectl port-forward --namespace spark svc/spark-release-master-svc 8081:80

go to URL: 127.0.0.1:8081


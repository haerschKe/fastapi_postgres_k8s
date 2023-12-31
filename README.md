# FastApi and Postgres Demo Project on Kubernetes
This is a basic demo project to deploy a FastApi frontend and Postgres backend on K8s (via Minikube).

## How to run

Note: the Servername of Postgres DB URL is changed to ServiceName of postgres-service, therefore the fastapi-secret was modified too due to the changed Servername
### Deployment without Ingress
```bash
kubectl apply -f db/postgres-secret.yaml
kubectl apply -f db/postgres-deployment.yaml 
kubectl apply -f db/postgres-service.yaml

kubectl apply -f app/fastapi-secret.yaml 
kubectl apply -f app/fastapi-deployment.yaml
kubectl apply -f app/fastapi-service.yaml 

minikube service --url fastapi-service
```
Copy the URL of **minikube service ...** to your browser and **/docs** to the path to view the FastApi Doc and run the exemplary REST calls.

For the demo everything is deployed in the default K8s namespace. 

Beware to deploy K8s secrets always first because they are used in deployments, etc. 

Clean everything in current (default) namespace:
```bash
kubectl delete all --all
```

### Deployment with Ingress
```bash
minikube addons enable ingress
kubectl get ns
kubectl get pods -n ingress-nginx

kubectl apply -f db/postgres-secret.yaml
kubectl apply -f db/postgres-deployment.yaml 
kubectl apply -f db/postgres-service.yaml

kubectl apply -f app/fastapi-secret.yaml 
kubectl apply -f app/fastapi-deployment.yaml
kubectl apply -f app/fastapi-ingress-service.yaml 

kubectl apply -f k8s/ingress/my-ingress.yaml 
```

### If you are on a Mac (with M machine and docker driver) do the following:

You won’t be able to access the ingress exposed services via minikube IP. You need to run minikube tunnel to make the service avaiable via local ip **127.0.0.1** instead. You will also need to map **myapp.example.com** (this is the host from my-ingress.yaml) to IP **127.0.0.1** instead of MINIKUBE IP in **/etc/hosts**:
```
127.0.0.1    myapp.example.com
```
Now you need to acess a tunnel for Minikube:
````
minikube tunnel
````

-----------
### If you are on any other machine do the following:

Get Minikube IP via  `minikube ip` or `kubectl get ingress` or `kubectl get nodes -o wide`.

Aftherwards add the Minikube IP to **/etc/hosts**: 
```
192.168.49.2   myapp.example.com (this is the host from my-ingress.yaml)
```

In both cases go to your browser and type **myapp.example.com/docs** to get to the FastAPI Doc.

-------
Clean everything:
```bash
kubectl delete all --all
kubectl delete all --all -n ingress-nginx
```

------

### Deployment with HELM
When running the basic k8s files be sure to deploy the **db** stuff before the **app** stuff to guarantee that the Postgres DB is running when the app wants to establish a connection. 

When running with HELM this is not guaranteed, therefore an **initContainers** is added to the **app deployment** to wait for until the Postgres DB is up and running before the app establishes the connection to the db.

To run via HELM, do the following:
```
cd charts
helm install myapp-demo fastapi-postgres

minikube tunnel

helm uninstall myapp-demo
```

-------


## ToDo:
- [ ] Persistence: PV, PVC, etc.
- [ ] ReadinessProbe, LivenessProbe

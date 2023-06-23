# fastapi_postgres_k8s

Code (in src/app) is from https://dev.to/ken_mwaura1/getting-started-with-fast-api-and-docker-515.

Example DevOps Project with FastApi: https://medium.com/@l.dergham/devops-project-part-4-92d6641ed752

Another larger Example is Jetbrains Fastapi/Docker/Kubernetes Example: 
https://www.jetbrains.com/pycharm/guide/tutorials/fastapi-aws-kubernetes/kubernetes_deploy/, https://github.com/mukulmantosh/FastAPI_EKS_Kubernetes


Before looking at a sample GitHub Action, we’ll familiarize ourselves with the syntax and terminology 
that we’ll encounter:

Workflow: A configurable automated process that will run one or more jobs. Workflows are defined 
by a YAML file within your repo and will run when triggered by an event in your repo. 
They can also be triggered manually, or with a defined schedule. Workflows are defined in 
the .github/workflows directory in a repo, and we can have multiple workflows per repo, 
each of which can perform a different set of tasks.

Event: An activity that triggers a workflow; these can be based on events such as push or pull requests, 
but they can also be scheduled using the crontab syntax.

Job: A task in a single workflow. A workflow may consist of one or more jobs, and all jobs need to 
execute without any errors in order for a workflow to be successful.

Step: A smaller task that is executed within a job. All steps must be completed in order to complete 
a job.

Action: A standalone command performed in a step. You can write your own Actions, or you can find 
Actions to use in your workflows in the GitHub Marketplace.

Runner: A server that runs your workflows when they’re triggered. Each runner can run a single 
job at a time. GitHub provides Ubuntu Linux, Microsoft Windows, and macOS runners for workflows; 
each workflow run executes in a fresh, newly-provisioned virtual machine.

## Example for Deplyoment and Service ()
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: django-app
  labels:
    app: django-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: django-app
  template:
    metadata:
      labels:
        app: django-app
    spec:
      containers:
        - name: django-app
          image: minikube-tutorial/mysite:v1.0
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          env:
            - name: POD_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP
            - name: HOST_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.hostIP
```

From the spec file:

- The `metadata: name` field describes the deployment name, whereas the `metadata: labels` describes the labels for the deployment i.e. can be thought of as a tagging mechanism.
- The `spec: replicas` field defines the number of pods to run.
- The `spec: selector: matchLabels` field describes what pods the deployment should apply to.
- The `spec: template: metadata:` labels field indicates what labels should be assigned to the running pod. This label is what is found by the matchLabels field in the deployment.
- The `spec: template: spec` field, contains a list of `containers` that belong to this pod. In this case it indicates the pod has one container as it only has one image and name in the list.
- The deployment exposes port `8000` within the pod as defined in the `spec: template: spec: containers: ports` field.
- there are too many different ways to pass envriment variables to your container but right now, we are using the simplest way because we do not have secrets, please check the [docs](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/).


```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
  namespace: default
spec:
  ports:
    - port: 8080
      protocol: TCP
      targetPort: 8080
  selector:
    app: django-app
  type: NodePort
```

- The `metadata: name` field describes the name of the Service object that will be created and can be identified by running `kubectl get svc`.
- The `spec: selector` field specifies the <pod_label> and <pod_value> that the service applies to. This means that any pod matching <pod_key>=<pod_value> label will be exposed by the service, in our case `pod_key` is `app` and `pod_value` is `django-app`
- The `spec: ports` contains a yaml array. The protocol in the first item in the array is TCP where the pod `port: 8000` field is exposed to the Kubernetes cluster i.e. the cluster interacts with the pod on port `8000`. The `targetPort` is the port within the pod that it’s exposed through. If port is not defined, it will default to the `targetPort` . The `NodePort` type instructs the service to expose the pod to the node/host machine on a random port in the default range `30000–32767` , however an explicit nodePort can be set in the protocols array to specify which port in the default range the host machine can communicate with the pod .

Get access port of service on minikube:
```yaml
kubectl get svc

minikube service --url <service_name>
```
Copy the URL of the URL-field in your browser to access it.
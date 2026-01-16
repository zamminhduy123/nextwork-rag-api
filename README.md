# RAG Systems 

# Requirements

python 3.13
ollama
tinyollama

### verify env
```pip list | grep -E "fastapi|uvicorn|chromadb|ollama"```

# Note
```
curl -X POST "http://127.0.0.1:8000/query" -G --data-urlencode "q=What is Docker Hub?"

    docker run --rm -p 8000:8000 -e OLLAMA_HOST="http://host.docker.internal:11434" network-rag-api
```

# Knowledges

💡 How does this RAG workflow work?
1. Receive question → 2. Search knowledge base with Chroma → 3. Get relevant context → 4. Combine context + question → 5. Send to Ollama's tinyllama → 6. Return AI-generated answer based on your documents

💡 What is Swagger UI?
Swagger UI is an automatically generated, interactive documentation page for your FastAPI server. It lets you visually explore your API's endpoints, see what parameters they accept, and even try them out right from your browser.

💡 Why a health endpoint?
Load balancers and orchestrators (like Kubernetes) ping /health to check if your app is ready to receive traffic.

💡 What is a Dockerfile?
A text file with instructions for building a Docker image. It specifies the base image, copies your code, installs dependencies, and defines how to run your app.

💡 What is a Docker image?
A Docker image is a portable package that contains your app's code, dependencies, and settings. Think of it like a blueprint or a recipe - it has everything your application needs to run, but it's not running yet.

💡 Image vs Container?
An image is a read-only template. A container is a running instance of an image.

💡 Why push to Docker Hub?
When you push your image to Docker Hub, anyone can pull and run it with a single command. This is essential for sharing work, deploying to production, CI/CD pipelines, and learning how container registries work (same concept as AWS ECR, Google Container Registry, etc.)

💡 What's the value of Docker Hub?
You can share it - Anyone can pull and run your image
CI/CD ready - Automated pipelines can pull your image
Multi-machine - Pull the same image on any machine with Docker
Version control - Tag different versions (v1.0, v1.1) and manage releases
This is how professional teams distribute containerized applications!

💡 Why do we start with Docker before Kubernetes?
Kubernetes can only run things that are already packaged.

Docker comes first because it packages your app and everything it needs into a container image - a single, portable unit that runs the same on any machine.

Kubernetes then uses that image to create and run containers. It decides where they run, how many to run, and keeps the containers alive - but it never builds the image itself.

💡 What does kubectl do?
Every interaction with Kubernetes goes through kubectl!

In this project, kubectl connects to the Kubernetes cluster that Minikube will create and lets you run commands to deploy apps, check status, view logs, and more.

# Kubernetes

💡 Extra for Experts: What does this output mean?
This is the structure of your kubectl config file, shown in YAML format! Here's what each field means:
- apiVersion: v1 - The version of the Kubernetes API this config file uses. This is standard and you don't need to change it.
- clusters: null - This is where cluster connection details will be stored. Right now it's empty (null) because we haven't created a cluster yet. Once Minikube starts, it will add your local cluster here!
- contexts: null - A context is a combination of a cluster, user, and namespace. It's like a "profile" that tells kubectl which cluster to connect to and how. This will be populated when Minikube sets up your cluster.
- current-context: "" - This shows which context is currently active. It's empty because there are no contexts yet!
- kind: Config - This tells Kubernetes that this is a configuration file (as opposed to a Deployment, Service, or other Kubernetes resource).
- users: null - This stores authentication information for different users. It's empty now, but Minikube will add authentication details when it creates the cluster.

💡 What's a Kubernetes cluster and why do we need one?
A Kubernetes cluster is the foundation that makes Kubernetes work - it's a set of machines (called nodes) that work together to run and manage your containerized applications.

You can't use Kubernetes without a cluster! Think of it like this: Docker runs containers on a single machine, but Kubernetes needs a cluster (even if it's just one node) to orchestrate containers across multiple machines, handle failures, scale up or down, and manage networking.

In production, clusters can have hundreds of nodes spread across data centers. Minikube creates a single-node cluster perfect for learning - it's still a real cluster, just smaller! This cluster will manage your RAG API containers - starting them, restarting them if they crash, scaling them when needed, and routing traffic to them.


💡 Extra for Experts: What services does Minikube start?
Minikube starts several core Kubernetes services that work together to manage your containers:
API Server - The "front desk" of Kubernetes that receives and processes all commands (like creating pods or deployments)
Scheduler - Decides which node (computer) should run each container
Controller Manager - Keeps track of the desired state of your cluster and makes sure everything matches
etcd - A database that stores all the configuration and state of your cluster
kube-proxy - Handles networking between containers and services
These services run as containers inside Minikube's virtual environment, working together to create a fully functional Kubernetes cluster on your computer!

💡 What are nodes in Kubernetes?
A node is a machine (physical or virtual) that runs your containers. Think of it like a worker in a factory - the node is where your containers actually execute.

In production, Kubernetes clusters have many nodes (hundreds of servers working together). But Minikube creates a single-node cluster - just one machine running on your laptop.

💡 What is a Docker daemon?
The Docker daemon is the background service that actually runs Docker containers and manages Docker images. Think of it as the "engine" that powers Docker - when you run commands like docker build or docker run, your terminal (the Docker CLI) sends instructions to the Docker daemon, which then does the actual work.


💡 What is a Kubernetes Deployment?
Think of it as a blueprint that tells Kubernetes how to run your app. Kubernetes will make sure your app always matches this blueprint - if a container crashes, Kubernetes automatically starts a new one. It:

- Specifies which container image to run
- Defines how many replicas (copies) to run
- Handles rolling updates (updating without downtime)
- Restarts containers if they crash
- Scales your application up or down

💡 Extra for Experts: How do Deployments work?
When you create a Deployment, Kubernetes:

- Creates a ReplicaSet (which manages the actual pods)
- The ReplicaSet creates Pods (running containers)
- If a Pod crashes, the ReplicaSet creates a new one
- If you update the Deployment, Kubernetes performs a rolling update (gradually replacing old pods with new ones)
This is how production systems stay available even when things go wrong!

💡 What is a Pod?
A Pod is the smallest deployable unit in Kubernetes. It's a group of one or more containers that share storage and network resources. In our case, each Pod will contain one container (your RAG API).

Think of a Pod like a "wrapper" around your container - Kubernetes doesn't run containers directly. Instead, it runs Pods, and Pods contain containers. This design allows Kubernetes to manage multiple containers together as a single unit, share networking and storage between them, and keep them on the same node.

When you create a Deployment (which we'll do next), Kubernetes will create Pods based on your Deployment's specifications. Each Pod runs your containerized RAG API, and Kubernetes manages these Pods - starting them, restarting them if they crash, and ensuring the right number are always running.

💡 How does a Service provide stable networking?
A Service provides:

- A stable IP address that never changes
- A DNS name (like rag-app-service) that always works
- Load balancing across multiple Pods (if you have replicas > 1)
- Automatic routing to healthy Pods

No matter how many times the Pods behind it restart, the Service always routes traffic to them correctly.

💡 What is NodePort and why do we need it?
NodePort is a way to make your Service accessible from outside your Kubernetes cluster.

💡 Why NodePort instead of other Service types?
- ClusterIP (default) - Only accessible from inside the cluster. Your laptop can't reach it!
- NodePort - Opens a port on each node, making it accessible from outside. Perfect for local development with Minikube!
- LoadBalancer - Requires cloud infrastructure (AWS, GCP, etc.). Not available in local Minikube.

NodePort is the simplest way to access your API from your laptop when using Minikube!
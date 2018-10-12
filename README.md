# Running Ray Cluster on Kubernetes
### Disclaimer:
Many thanks to the instructions by Robert and Charles: found on [here](https://github.com/robertnishihara/ray-kubernetes/blob/instructions/README.md)
## Instructions
**For most up-to-date set-up instructions:** [Medium Blog Post](https://medium.com/@apengjh/4634a51effc9)

ray-project [here](https://github.com/ray-project/ray)
#### Setup Google Cloud and Install Cloud SDK
Follow instructions from Google [here](https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu) to install Cloud SDK for Ubuntu.

Create a new project on [Google Cloud Console](console.cloud.google.com) and start a Kubernetes Cluster in that project.

Run `gcloud init` and follow the prompted instructions

Install `kubectl` on your local machine using either `gcloud components install kubectl` or  ([Instructions](https://kubernetes.io/docs/tasks/tools/install-kubectl/))

On your [GCloud Console](console.cloud.google.com) goto ->Project->Kubernetes Engine->Clusters and click on `Connect`. Paste the code to command-line to give `kubectl` access to your cluster.
#### Build and Push Docker Image

Clone the [repository](https://github.com/jhpenger/ray-kubernetes): `git clone https://github.com/jhpenger/ray-kubernetes.git`

Edit `build.sh`, `head.yml`, `worker.yml`: replace `tutorial-218804` with your project-ID

Run:
```sh
bash build.sh
```
```
docker push <image-tag>
```
#### Deploying Pods on Kubernetes Cluster
In the cloned repository:
```
kubectl create -f head.yml
```
Wait for the `ray-head` pod to be fully running. You can check pods' status with `kubectl get pods`. If your head pod crashes `kubectl logs ray-head` to debug.

Obtain `ray-head`'s Public Key by either:
1. `kubectl logs ray-head` (key will be near bottom of output)
2. `kubectl exec -it ray-head bash`; Then
`more ~/.ssh/id_rsa.pub`

Edit `worker.yml`: replace `<PASTE-PUBKEY-HERE-ONELINE>` with `ray-head`'s Public Key

If you are in `ray-head`, exit back to your local machine and run:
```
kubectl create -f worker.yml
```

#### Testing Your Cluster
I mounted a simple python script (modified from `exercise04.ipynb` found [here](https://github.com/ray-project/tutorial/blob/master/exercises/exercise04.ipynb)) to test the cluster.
First, get into your `ray-head` with `kubectl exec -it ray-head bash`. Then run:
```
python /ray-kubernetes/test_cluster.py $MY_POD_IP:6379
```
You can choose to define # of actors by passing in an additional parameter. (e.g. `python /ray-kubernetes/test_cluster.py $MY_POD_IP:6379 8888`). Default is set to 136. `#-of-actors` should be no more than `# of CPU cores` in your cluster (`not # of CPUs`)
Your expected run-time should be ~`2.5` seconds, but might be slower due to reaching cluster's max CPU capacity.

# Notes
Instructions setup for Koç Lab @ University of California Santa Barbara.

We are trying to utilize Ray cluster to do reinforcement learning on [Gibson Enviroment](http://gibsonenv.stanford.edu/).

Currently in the very early stages of exploring `ray` and `Gibson`. Would greately appreciate guidance from anyone with:
* experience in running reinforcement earning simulations on large clusters using `GCloud` or `AWS`.
* using Google's `Preemptible VM Instances` with `ray` to cut down costs. Specifically in dealing with what to do when `pre-emptible instance` restarts.

Contact [Sam](mailto:samgreen@gmail.com) and [Jun](mailto:peng00@cs.ucsb.edu)
Thanks,

Contact me @ [peng00@cs.ucsb.edu](mailto:peng00@cs.ucsb.edu)

import ray
import time
import sys

if len(sys.argv) != 3:
    print ("Usage: python get_pods.py <redis-address> <path-to-workers.txt>")
    exit()

ray.init(redis_address=sys.argv[1])
@ray.remote
def f():
    time.sleep(0.01)
    return ray.services.get_node_ip_address()

# Get a list of the IP addresses of the nodes that have joined the cluster.
pods = set(ray.get([f.remote() for _ in range(1000)]))
print(pods)
print("Size of this cluster = %d" %len(pods))
pods.remove(sys.argv[1][:-5])
workerFile = open(sys.argv[2], "w")
for pod in pods:
    workerFile.write(pod + "\n")
workerFile.close()
print("Workers' IP saved to %s" %sys.argv[2])

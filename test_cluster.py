from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import ray
import time
import sys

if 3 < len(sys.argv) < 2:
    print("Usage: python test_cluster.py <redis-address> <#-of-ray-actors>")
    print("<#-of-ray-actors> OPTIONAL, default = 136")
    exit()

ray.init(sys.argv[1])

@ray.remote
class Foo(object):
    def __init__(self):
        self.counter = 0

    def reset(self):
        self.counter = 0

    def increment(self):
        time.sleep(0.5)
        self.counter += 1
        return self.counter

try:
    num_of_actors = int(sys.argv[3])
except:
    num_of_actors = 68*2
Foos = [Foo.remote() for _ in range(num_of_actors)]



time.sleep(2.0)


# Reset the actor state so that we can run this cell multiple times without
# changing the results.
for f in Foos:
    f.reset.remote()

# We want to parallelize this code. However, it is not straightforward to
# make "increment" a remote function, because state is shared (the value of
# "self.counter") between subsequent calls to "increment". In this case, it
# makes sense to use actors.
results = []
start_time = time.time()
for _ in range(5):
    for f in Foos:
        results.append(f.increment.remote())

results = ray.get(results)
end_time = time.time()
duration = end_time - start_time



#assert results == [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]

#assert duration < 3, ('The experiments ran in {} seconds. This is too '
#                      'slow.'.format(duration))
#assert duration > 2.5, ('The experiments ran in {} seconds. This is too '
#                        'fast.'.format(duration))

print(results)
print("Usage: python test_cluster.py <redis-address> <#-of-ray-actors> \n <#-of-ray-actors> OPTIONAL, default = 136")
print('Success! The example took {} seconds.'.format(duration))
print('Num of ray actors = %d' %num_of_remote_functions)

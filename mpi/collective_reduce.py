from mpi4py import MPI
import time
import math

t0 = time.time()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()

# number of integration steps
nsteps = 10000000
# step size
dx = 1.0 / nsteps

if rank == 0:
    # determine the size of each sub-task
    ave, res = divmod(nsteps, nprocs)
    counts = [ave + 1 if p < res else ave for p in range(nprocs)]

    # determine the starting and ending indices of each sub-task
    starts = [sum(counts[:p]) for p in range(nprocs)]
    ends = [sum(counts[:p+1]) for p in range(nprocs)]

    # save the starting and ending indices in data  
    data = [(starts[p], ends[p]) for p in range(nprocs)]
else:
    data = None

data = comm.scatter(data, root=0)

# compute partial contribution to pi on each process
partial_pi = 0.0
for i in range(data[0], data[1]):
    x = (i + 0.5) * dx
    partial_pi += 4.0 / (1.0 + x * x)
partial_pi *= dx

pi = comm.reduce(partial_pi, op=MPI.SUM, root=0)

if rank == 0:
    print('pi computed in {:.3f} sec'.format(time.time() - t0))
    print('error is {}'.format(abs(pi - math.pi)))
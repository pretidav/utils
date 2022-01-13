from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# master process
if rank == 0:
    data = {'x': 1, 'y': 2.0}
    for i in range(1, size):
        req = comm.isend(data, dest=i, tag=i)
        req.wait()
        print('Process {} sent data:'.format(rank), data)

else:
    req = comm.irecv(source=0, tag=rank)
    data = req.wait()
    print('Process {} received data:'.format(rank), data)
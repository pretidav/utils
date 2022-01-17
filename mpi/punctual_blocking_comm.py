from mpi4py import MPI
class C():
    def __init__(self,comm):
        self.comm = comm 
        self.ciao = 0
    def func(self):
        # master process
        if rank == 0:
            data = {'x': 1, 'y': 2.0}
            # master process sends data to worker processes by
            # going through the ranks of all worker processes
            for i in range(1, size):
                self.comm.send(data, dest=i, tag=i)
                print('Process {} sent data:'.format(rank), data)

        # worker processes
        else:
            # each worker process receives data from master process
            data = self.comm.recv(source=0, tag=rank)
            print('Process {} received data:'.format(rank), data)


if __name__=='__main__':
    #global comm 
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    CC = C(comm)
    CC.func()

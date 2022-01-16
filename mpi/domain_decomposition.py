from mpi4py import MPI, rc
import numpy as np
import argparse

if __name__=='__main__': 
    parser = argparse.ArgumentParser()

    parser.add_argument('--grid', help='dimensions', default='4x4' )
    parser.add_argument('--pgrid', help="XxY...", default="1x2")
    args = parser.parse_args()
    pgrid = [int(a) for a in str(args.pgrid).split('x')]
    grid = [int(a) for a in str(args.grid).split('x')]


    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    dim = len(pgrid)
    periodiciy = [True]*dim
    cartesian2d = comm.Create_cart(dims = pgrid, periods = periodiciy,reorder=False)
    coord2d = cartesian2d.Get_coords(rank)
    print ("In "+str(dim)+"D topology, Processor ",rank, " has coordinates ",coord2d)

    lattice=np.zeros(shape=tuple(grid))+rank
    print('processor {} lattice \n {}'.format(rank,lattice))

    cartesian2d.barrier()

    (left,right)= tuple(MPI.Cartcomm.Shift(cartesian2d,0,1))
    print('processor {} left,right {}-{}'.format(rank,left,right))

    sum=0
    snd_buf=np.array(lattice[-1],dtype='float')
    rcv_buf = snd_buf
    cartesian2d.Sendrecv([snd_buf, MPI.FLOAT],right,0,[rcv_buf, MPI.FLOAT],left,0)  
    
    #cartesian2d.barrier()
    print('processor {} rcv_buf {}'.format(rank,rcv_buf))
    cartesian2d.barrier() 
    lattice[0]=rcv_buf
    print('processor {} shifted lattice \n {}'.format(rank,lattice))
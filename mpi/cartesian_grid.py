from mpi4py import MPI
import numpy as np

# This is to create default communicator and get the rank
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
cartesian2d = comm.Create_cart(dims = [2,2],periods =[False,False],reorder=False)
coord2d = cartesian2d.Get_coords(rank)
print ("In 2D topology, Processor ",rank, " has coordinates ",coord2d)

# Get coordinates of your neighbour to left and right
left,right = cartesian2d.Shift(direction = 0, disp=1)
print("Processor ",rank, "has his neighbour", left, " and ",right )

#Create a sub-communicator slice
cartesian1d = cartesian2d.Sub(remain_dims=[False,True])
rank1d = cartesian1d.Get_rank()
coord1d = cartesian1d.Get_coords(rank1d)
print ("In 1D topology, Processor ",rank,"  has coordinates ", coord1d) 
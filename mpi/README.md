### install OpenMPI 
if c++ compiler is not present: 
~~~
sudo apt-get install g++
~~~

if make is not present: 
~~~
sudo apt install make
~~~
then: 
~~~
https://edu.itp.phys.ethz.ch/hs12/programming_techniques/openmpi.pdf
~~~

### install mpi4py
~~~
conda install -c conda-forge mpi4py openmpi
~~~

## NOTE
mpi takes advantage of physical CPUs only. 
This number can be checked with 
~~~
import psutil 
print(psutil.cpu_count(logical=False))
~~~


# Useful examples (see docs/)
~~~
https://github.com/jbornschein/mpi4py-examples
~~~

# Cartcomm 
~~~
https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Cartcomm.html#mpi4py.MPI.Cartcomm
https://learn2codewithmesite.wordpress.com/2017/10/16/creating-topologies-in-mpi4py/
~~~
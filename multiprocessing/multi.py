from threading import Thread, Lock, Barrier
from multiprocessing import BoundedSemaphore, cpu_count, Pool
import time
from random import randint
from queue import Queue
from tqdm import tqdm
import numpy as np

#https://www.html.it/pag/69486/multithreading/

class myThread_async(Thread):
   def __init__(self, nome, durata):
      Thread.__init__(self)
      self.nome = nome
      self.durata = durata
   def run(self):
      print ("Thread '" + self.name + "' start")
      time.sleep(self.durata)
      print ("Thread '" + self.name + "' end")


threadLock = Lock()
class myThread_sync(Thread):
   def __init__(self, nome, durata):
      Thread.__init__(self)
      self.nome = nome
      self.durata = durata
   def run(self):
      print ("Thread '" + self.name + "' start")
      # Acquisizione del lock
      threadLock.acquire()
      print("Thread '" + self.name + "' lock acquired")
      time.sleep(self.durata)
      print ("Thread '" + self.name + "' end")
      # Rilascio del lock
      threadLock.release()
      print("Thread '" + self.name + "' lock released")


barrier = Barrier(3,timeout=10)
class myThread_barrier(Thread):
    def __init__(self, nome, durata):
        Thread.__init__(self)
        self.nome = nome
        self.durata = durata
    def run(self):
        print ("Thread '" + self.name + "' start")
        # Acquisizione del lock
        time.sleep(self.durata)
        print("Parties = " + str(barrier.parties) + "\n")
        print("n_waiting = " + str(barrier.n_waiting) + "\n")
        barrier.wait()
        print ("Thread '" + self.name + "' end")
        

bsemaphore = BoundedSemaphore(2)
class myThread_boundsemaphore(Thread):
    def __init__(self, nome, durata):
        Thread.__init__(self)
        self.nome = nome
        self.durata = durata
    def run(self):
        print ("Thread '" + self.name + "' start")
        # Acquisizione del lock
        bsemaphore.acquire()
        print("Thread '" + self.name + "' semaphore acquired")
        time.sleep(self.durata)
        print ("Thread '" + self.name + "' end")
        # Rilascio del lock
        bsemaphore.release()
        print("Thread '" + self.name + "' semaphore released")

        

def start(Th,n):
    # Creazione dei thread
    threads = []
    if n>cpu_count():
        print('too many threads.. maximum is {}'.format(cpu_count()))
        exit(0)
    threads = [Th("Thread#"+str(i), randint(1,10)) for i in range(n)] 
    # Avvio dei thread
    for th in threads:  
        th.start()      #execute run() method 
    # Join
    for th in threads:
        th.join()       #until all these threads are over, the code does not proceed further. 
    print("Fine")


def myfunc(name,a,b,c):
    print('started thread #{}'.format(name))
    time.sleep(10)
    print(a,b,c)
    print('ended thread #{}'.format(name))

def myfuncqueue(name,q):
    while not q.empty():
        work = q.get() 
        print('process #{} work {}'.format(name,work))
        time.sleep(5)
        q.task_done()
    return True

def cube(x):
    return x**3

if __name__=='__main__':
    N=8
    print('# ASYNC #')
    start(Th=myThread_async,n=N)
    print('# SYNC #')
    start(Th=myThread_sync,n=N)
    print('# BARRIER #')
    start(Th=myThread_barrier,n=3)
    print('# BOUNDED SEMAPHORE #')
    start(Th=myThread_boundsemaphore,n=5)
    


    print('# FUNCTION THREAD #')
    N=2
    alist = [1,2]
    blist = ['a','b']
    clist = ['g','e']
    processes = []
    for i in range(N):
        process = Thread(target=myfunc, args=[i,alist[i],blist[i],clist[i]])
        process.start()
        processes.append(process)
    for process in processes:
        process.join()

    print('# QUEUE THREADS')  #if you need more than cpu_count() threads! 
    #https://www.shanelynn.ie/using-python-threading-for-multiple-results-queue/

    M=20
    q = Queue(maxsize=0)
    num_theads = min(M, cpu_count())
    alist = [i for i in range(M)]
    blist = [i*100 for i in range(M)]
    clist = [i*1000 for i in range(M)]
    for i in range(M):
        q.put((i,[alist[i],blist[i],clist[i]]))   #create a queue of threads
    for i in range(num_theads):
        process = Thread(target=myfuncqueue, args=[str(i),q]) 
        process.start()
    q.join() #threads are executed until all the queue is empty


    print('##### POOL ######')

    print('# POOL apply')
    pool = Pool(processes=4)
    results = [pool.apply(cube, args=(x,)) for x in range(1,7)]
    print(results)

    print('# POOL amap')
    pool = Pool(processes=4)
    results = pool.map(cube, range(1,7))
    print(results)

    print('# POOL apply async')
    pool = Pool(processes=4)
    results = [pool.apply_async(cube, args=(x,)) for x in range(1,7)]
    output = [p.get() for p in results]
    print(output)

    print('# POOL imap')
    rr = list(np.arange(1,7,1))
    with Pool(processes=4) as p:
        A=list(tqdm(p.imap(cube, rr),total=len(rr)))
    print(A)


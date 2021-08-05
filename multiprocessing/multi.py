from threading import Thread, Lock
from multiprocessing import cpu_count
import time
from random import randint
from queue import Queue


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

if __name__=='__main__':
    N=8
    print('# ASYNC #')
    start(Th=myThread_async,n=N)
    print('# SYNC #')
    start(Th=myThread_sync,n=N)

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


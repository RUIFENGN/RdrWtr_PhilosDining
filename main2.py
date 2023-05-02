import threading
import time
import random
import tkinter as tk
from tkinter import messagebox
from P_V import semaphore
from thread import MyThread

# 定义资源和信号量
num_philosophers = 5
Mutex_forks = [semaphore(1),semaphore(1),semaphore(1),semaphore(1),semaphore(1)]  # 叉子信号量，1表示可用，此外则等待
forks = [1] * num_philosophers # 叉子资源，1表示可用，0表示被占用

# 创建非死锁哲学家的线程
def Philosopher_notDeadLock(i,mutexLeftFork,mutexRightFork,leftfork,rightfork):
    while 1:
        # 随机休息1-3s
        print("哲学家" + str(i) + "在休息")
        time.sleep(random.randint(1,3))
        print("哲学家" + str(i) + "休息完毕，正在等待")
        # 等待
        thread_lf = MyThread(0)
        thread_rf = MyThread(0)
        #print(mutexLeftFork.value,mutexRightFork.value)
        #print(mutexLeftFork == mutexRightFork)
        # 判断资源
        if leftfork == 1 & rightfork == 1:
            # 占用资源
            mutexLeftFork.P_P_l(thread_lf,i) # 排队使用leftfork
            #print(mutexLeftFork.value,mutexRightFork.value)
            mutexRightFork.P_P_r(thread_rf,i) # 排队使用rightfork
            # 修改资源值
            forks[i] = 0
            forks[(i+1)%num_philosophers] = 0
            # 吃通心粉
            print("哲学家" + str(i) + "在吃通心粉")
            time.sleep(random.randint(1,3))
            # 释放资源
            forks[i] = 1
            forks[(i + 1) % num_philosophers] = 1
            mutexLeftFork.V()
            mutexRightFork.V()

# messagebox实现筛选是否死锁以及死锁时间

# 创建死锁哲学家的线程
def Philosopher_shortDeadLock(i,mutexLeftFork,mutexRightFork,leftfork,rightfork):
    while 1:
        # 随机休息1-3s
        print("哲学家" + str(i) + "在休息")
        random.seed(1000+i)
        time.sleep(random.randint(1,3))
        print("哲学家" + str(i) + "休息完毕，正在等待")
        # 等待
        thread_lf = MyThread(0)
        thread_rf = MyThread(0)
        #print(mutexLeftFork.value,mutexRightFork.value)
        #print(mutexLeftFork == mutexRightFork)
        while 1:
            if leftfork == 1:
                mutexLeftFork.P_P_l(thread_lf,i) # 排队使用leftfork
                forks[i] = 0
                time.sleep(random.randint(1,5))
                if rightfork == 1 :
                    mutexRightFork.P_P_r(thread_rf, i)  # 排队使用rightfork
                    forks[(i+1)%num_philosophers] = 0
                #print(mutexLeftFork.value,mutexRightFork.value)

                    # 吃通心粉
                    print("哲学家" + str(i) + "在吃通心粉")
                    time.sleep(random.randint(0,1))
                    # 释放资源
                    leftfork = 1
                    rightfork = 1
                    mutexLeftFork.V()
                    mutexRightFork.V()
                    break

# 创建死锁哲学家的线程
def Philosopher_longDeadLock(i,mutexLeftFork,mutexRightFork,leftfork,rightfork):
    while 1:
        # 随机休息1-3s
        print("哲学家" + str(i) + "在休息")
        random.seed(1000+i)
        time.sleep(random.randint(0,2))
        print("哲学家" + str(i) + "休息完毕，正在等待")
        # 等待
        thread_lf = MyThread(0)
        thread_rf = MyThread(0)
        #print(mutexLeftFork.value,mutexRightFork.value)
        #print(mutexLeftFork == mutexRightFork)
        while 1:
            if leftfork == 1:
                mutexLeftFork.P_P_l(thread_lf,i) # 排队使用leftfork
                forks[i] = 0
                time.sleep(random.randint(0,2))
                if rightfork == 1 :
                    mutexRightFork.P_P_r(thread_rf, i)  # 排队使用rightfork
                    forks[(i+1)%num_philosophers] = 0
                #print(mutexLeftFork.value,mutexRightFork.value)

                    # 吃通心粉
                    print("哲学家" + str(i) + "在吃通心粉")
                    time.sleep(random.randint(0,1))
                    # 释放资源
                    leftfork = 1
                    rightfork = 1
                    mutexLeftFork.V()
                    mutexRightFork.V()
                    break

# 判断死锁的方式，并输出死锁的时间

# messagebox选择是否死锁并设置死锁的时间长短
is_deadlock = messagebox.askyesno('Philosopher Dining Problem', '运行死锁模式还是非死锁模式 [yes/no]')
if is_deadlock:
    dead_time = messagebox.askyesno('Philosopher Dining Problem', ' 死锁时间短或是长 [yes/no]')
    if dead_time:
        # 创建5个哲学家，依次开启5个线程
        threads = []
        for i in range(num_philosophers):
            args = (i, Mutex_forks[i], Mutex_forks[(i + 1) % num_philosophers], forks[i], forks[(i + 1) % num_philosophers])
            thread = threading.Thread(target=Philosopher_shortDeadLock, args=args)
            threads.append(thread)

        for thread in threads:
            thread.start()
    else:
        # 创建5个哲学家，依次开启5个线程
        threads = []
        for i in range(num_philosophers):
            args = (
            i, Mutex_forks[i], Mutex_forks[(i + 1) % num_philosophers], forks[i], forks[(i + 1) % num_philosophers])
            thread = threading.Thread(target=Philosopher_longDeadLock, args=args)
            threads.append(thread)

        for thread in threads:
            thread.start()
else:
    # 创建5个哲学家，依次开启5个线程
    threads = []
    for i in range(num_philosophers):
        args = (i, Mutex_forks[i], Mutex_forks[(i+1) % num_philosophers], forks[i], forks[(i+1)%num_philosophers])
        thread = threading.Thread(target=Philosopher_notDeadLock, args=args)
        threads.append(thread)

    for thread in threads:
        thread.start()




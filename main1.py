from P_V import semaphore
from thread import MyThread
import time
import threading
import random

# 定义信号量资源
ReadCount = 0
Mutex_ReadCount = semaphore(1)
Mutex_BUF = semaphore(1)

def Reader(i):
    global ReadCount
    while 1:
        # 阅读者计数器登记
        print('阅读者'+str(i)+'登记')
        thread_MRC = MyThread(0)
        Mutex_ReadCount.P(thread_MRC)
        ReadCount += 1
        time.sleep(1)
        # 第一个阅读者申请buf
        thread_BF = MyThread(0)
        if ReadCount == 1 :
            Mutex_BUF.P(thread_BF)
            print('阅读者'+str(i)+"申请buf")
        Mutex_ReadCount.V()
        # 读文件
        print('阅读者'+str(i)+'在读文件')
        time.sleep(1)
        # 阅读者计数器注销
        thread_MRC = MyThread(0)
        Mutex_ReadCount.P(thread_MRC)

        ReadCount -= 1
        if ReadCount == 0 :
            Mutex_BUF.V()
            print('阅读者'+str(i)+"释放BUF")
        Mutex_ReadCount.V()
        wait_time = random.randint(1, 3)
        time.sleep(wait_time) #随机等待

def Writer(i):
    global Mutex_BUF
    while 1:
        thread_BF = MyThread(0)
        Mutex_BUF.P_W(thread_BF,i)
        # 写文件
        print('写者'+str(i)+'在写文件')
        # 释放BUF
        Mutex_BUF.V()
        wait_time = random.randint(1, 3)
        time.sleep(wait_time)  # 随机等待

# 创建五个读者，五个写者
threads = []
for i in range(5):
    args = (i,)
    threads.append(threading.Thread(target=Reader,args=args))
for i in range(5):
    args = (i,)
    threads.append(threading.Thread(target=Writer,args=args))

for thread in threads:
    thread.start()






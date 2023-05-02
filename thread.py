import threading

class MyThread(threading.Thread):
    def __init__(self, sleep_time):
        # 调用父类的构造方法
        super().__init__()
        self.sleep_time = sleep_time
        self.is_running = True
        self.cond = threading.Condition()

    def run(self):
        while self.is_running:
            with self.cond:
                self.cond.wait(timeout=self.sleep_time)
            print("{}: Woken up after {} seconds".format(self.name, self.sleep_time))

    def sleep(self):
        with self.cond:
            self.cond.wait()

    def wakeup(self):
        with self.cond:
            self.cond.notify()

    def stop(self):
        self.is_running = False
        self.wakeup()

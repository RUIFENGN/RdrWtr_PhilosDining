class semaphore:
    def __init__(self,value):
        self.value = value
        self.list = []
    def P(self,thread):
        self.value -= 1
        if self.value < 0 :
            self.list.append(thread)
            thread.sleep()

    def P_R(self,thread,i):
        self.value -= 1
        if self.value < 0 :
            self.list.append(thread)
            print("读者" + str(i) + "在排队")
            thread.sleep()


    def V(self):
        self.value += 1
        if self.value <= 0:
            p = self.list.pop(0)
            p.wakeup()

    def P_W(self,thread,i):
        self.value -= 1
        if self.value < 0 :
            self.list.append(thread)
            thread.sleep()
            print("写者" + str(i) + "在排队")

    def P_P_l(self,thread,i):
        self.value -= 1
        if self.value < 0 :
            self.list.append(thread)
            print("哲学家" + str(i) + "在排队等左边叉子")
            thread.sleep()


    def P_P_r(self, thread, i):
        self.value -= 1
        if self.value < 0:
            self.list.append(thread)
            print("哲学家" + str(i) + "在排队等右边叉子")
            thread.sleep()

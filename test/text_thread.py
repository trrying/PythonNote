import threading
import time


# def print_num(thread_name, data_list):
#     for data in data_list:
#         print(data)
#         time.sleep(1)
#
#
# try:
#     _thread.

class MyThread (threading.Thread):
    def __init__(self, thread_id, data_list):
        threading.Thread.__init__(self)
        self.threadId = thread_id
        self.dataList = data_list

    def run(self):
        for data in self.dataList:
            print(self.threadId + str(data))
            time.sleep(1)


thread1 = MyThread("1 ", range(10))
thread1.start()
thread1 = MyThread("2 ", range(10))
thread1.start()
thread1 = MyThread("3 ", range(10))
thread1.start()
thread1 = MyThread("4 ", range(10))
thread1.start()

































import threading

class MyThread(threading.Thread):
    def __init__(self, func, arg1, arg2):
        super().__init__()
        self.func = func
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = None

    def run(self):
        # 스레드에서 실행될 코드
        self.result = self.func(self.arg1, self.arg2)

    def get_result(self):
        return self.result
      
      
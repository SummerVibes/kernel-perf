from abc import ABCMeta, abstractmethod
from multiprocessing import Process
import time


class PerfTask(Process, metaclass=ABCMeta):
    name="Your Perf Task Name"

    def __init__(self, single_result):
        super().__init__()
        self.perf_result = single_result
    #       pre_run
    #      /        \
    #     run       monitor
    #      \        /
    #       post_run
    
    # Put your prepare steps here.
    @abstractmethod
    def pre_run(self):
        pass
    
    # Will be scheduled in a dependant thread.
    @abstractmethod
    def run(self):
        pass
    
    # Will be called repeated until run thread end up, this function must return a Stat
    @abstractmethod
    def monitor(self, tid, interval) -> dict:
        pass
    
    # Some clean up work should be here.
    @abstractmethod
    def post_run(self):
        pass

    # Used to parse perf result, must return a dict because we need json.
    @abstractmethod
    def parse(self, data) -> dict:
        pass

    def run_hook(self):
        print("Wait ftrace start.....")
        time.sleep(3)

    def get_pid_for_monitor(self):
        return self.task.pid
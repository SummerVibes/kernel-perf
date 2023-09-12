import json
import os
import subprocess
import time
from task.docker import DockerPerf
from task.mem_lb import MemoryLBPerf
from task.mem_ls import MemoryLSPerf
from task.mem_real import MemoryRealPerf
from task.mem_sb import MemorySBPerf
from task.mem_ss import MemorySSPerf
from task.perf_task import PerfTask
from task.redis import RedisPerf
import multiprocessing as mp
from task.xsbench import XSBenchPerf
import tools

class TaskRunner():
    # Default monitor interval is 1s
    def __init__(self, task: PerfTask, interval=1):
        self.task = task
        self.task_name = task.name
        self.interval = interval
        self.task_result = all_perf_result[self.task_name] = {}
        self.task_result["result"] = {}
        self.metric = self.task_result["metric"] = []

    def start(self):
        # prepare
        print(f"======================= Prepare for {self.task_name} =======================")
        try:
            self.task.pre_run()
        except subprocess.CalledProcessError as e:
            print(e.output)
            self.task_result["result"]["Error"] = str(e.output)
            return
        # run
        print(f"======================= Run for {self.task_name} ===========================")
        alloced = int(os.system("cat /proc/zoneinfo | grep nr_zero_page_alloc_total | awk '{print $1}'"))
        alloced_zero = int(os.system("cat /proc/zoneinfo | grep nr_zero_page_alloc_prezero | awk '{print $1}'"))
        self.task.start()
        #functions = ["do_anonymous_page", "do_huge_pmd_anonymous_page"]
        functions = ["do_anonymous_page"]
        pid = self.task.get_pid_for_monitor()
        tools.start_trace(pid, functions)
        # monitor
        print(f"======================= Monitor for {self.task_name} =======================")
        while self.task.is_alive():
            res=self.task.monitor(pid, self.interval)
            res['time'] = tools.get_cur_time()
            self.metric.append(res)
        alloced = alloced - int(os.system("cat /proc/zoneinfo | grep nr_zero_page_alloc_total | awk '{print $1}'"))
        alloced_zero = alloced_zero - int(os.system("cat /proc/zoneinfo | grep nr_zero_page_alloc_prezero | awk '{print $1}'"))
        # end / cleanup
        print(f"======================= Cleanup for {self.task_name} =======================")
        print(f"alloced: {alloced}, alloced_zero: {alloced_zero}, hit: {alloced_zero/alloced}%")
        tools.end_trace(functions)
        self.task_result["result"] = single_result.copy()
        single_result.clear()
        try:
            self.task.post_run()
        except subprocess.CalledProcessError as e:
            print(e.output)
            return

all_perf_result = {}
# all_perf_result['system_info'] = tools.system_info()

manager=mp.Manager()
single_result=manager.dict()

TaskRunner(MemoryLBPerf(single_result)).start()
TaskRunner(MemoryLSPerf(single_result)).start()
TaskRunner(MemorySBPerf(single_result)).start()
TaskRunner(MemorySSPerf(single_result)).start()
TaskRunner(MemoryRealPerf(single_result)).start()
TaskRunner(RedisPerf(single_result)).start()
# TaskRunner(DockerPerf(single_result)).start()
# TaskRunner(VmPerf(single_result)).start()
# TaskRunner(XSBenchPerf(single_result)).start()

with open(f"perf-{time.strftime('%d-%H-%M-%S', time.localtime())}.json", 'x') as f:
    json.dump(all_perf_result, f)

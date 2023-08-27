import subprocess
import tools
import re
from task.perf_task import PerfTask
class CPUPerf(PerfTask):
    name = "cpu"

    def pre_run(self):
        pass
    
    def run(self):
        self.run_hook()
        data = tools.run_shell("cpu.sh")
        self.perf_result["Success"] = self.parse(data)

    def parse(self, data) -> dict:
        # speed = re.search(r'events per second: ([0-9.]*)', data).group(1)
        return {
            "CPU Speed": data
        }
    
    def monitor(self, pid, interval) -> dict:
        stat = {
            "mem_stat" : tools.mem_stat(pid),
            "cpu_stat": tools.cpu_stat(interval),
        }
        return stat
    
    def post_run(self):
        pass
import subprocess
import tools
import re
from task.perf_task import PerfTask
class MemoryPerf(PerfTask):
    name = "memory"

    def pre_run(self):
        tools.run_shell("pgfault/prepare.sh")
    
    def run(self):
        self.run_hook()
        data = tools.run_shell("pgfault/run.sh")
        self.perf_result["Success"] = self.parse(data)

    def parse(self, data) -> dict:
        return {
            "Memory Result": data
        }
    
    def monitor(self, pid, interval) -> dict:
        stat = {
            "cpu_stat": tools.cpu_stat(interval),
        }
        return stat
    
    def post_run(self):
        pass
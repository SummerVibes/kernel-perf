import subprocess
import tools
import re
from task.perf_task import PerfTask
class JavaPerf(PerfTask):
    name = "java"

    def pre_run(self):
        pass
    
    def run(self):
        data = tools.run_shell("java.sh")
        self.perf_result["Success"] = self.parse(data)

    def parse(self, data) -> dict:
        return data
    
    def monitor(self, pid, interval) -> dict:
        stat = {
            "cpu_stat": tools.cpu_stat(interval),
        }
        return stat
    
    def post_run(self):
        pass
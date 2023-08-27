import subprocess
import tools
import re
from task.perf_task import PerfTask
class RedisPerf(PerfTask):
    name = "redis"

    def pre_run(self):
        pass
    
    def run(self):
        data = tools.run_shell("redis.sh")
        self.perf_result["Success"] = self.parse(data)

    def parse(self, data) -> dict:
        # speed = re.search(r'([0-9.]*) MiB/sec', data).group(1)
        return data
    
    def monitor(self, pid, interval) -> dict:
        stat = {
            "cpu_stat": tools.cpu_stat(interval),
        }
        return stat
    
    def post_run(self):
        pass
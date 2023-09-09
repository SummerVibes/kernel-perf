import tools
from task.perf_task import PerfTask
class VmPerf(PerfTask):
    name = "vm"

    def pre_run(self):
        pass
    
    def run(self):
        self.run_hook()
        data = tools.run_shell("vmm/vm.sh")
        self.perf_result["Success"] = self.parse(data)

    def parse(self, data) -> dict:
        return data
    
    def monitor(self, pid, interval) -> dict:
        stat = {
            "cpu_stat": tools.cpu_stat(interval),
            "mem_stat": tools.mem_stat(pid)
        }
        return stat
    
    def post_run(self):
        pass
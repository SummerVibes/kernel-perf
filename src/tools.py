import os
import sys
import time
import psutil
import subprocess
import json
import platform

def system_info():
    with os.popen("lshw -json") as f:
        data = json.loads(f.read())
        data['kernel'] = subprocess.check_output("uname -r".split(" ")).decode()
        return data

# return a array
def cpu_freq():
    freqs = psutil.cpu_freq(percpu=True)
    return [freq.current / 1000.0 for freq in freqs]

# return a json
def cpu_mpstat(interval) -> dict:
    sh="mpstat -o JSON -P ALL {} 1".format(interval)
    data = subprocess.check_output(sh.split(" "))
    return json.loads(data)['sysstat']['hosts'][0]

def cpu_stat(interval) -> dict:
    freq=cpu_freq()
    stat=cpu_mpstat(interval)
    all_cpu_load=stat['statistics'][0]['cpu-load'][0]
    per_cpu_load=stat['statistics'][0]['cpu-load'][1:]
    if platform.machine() == 'x86_64':
        for index, item in enumerate(per_cpu_load):
            item['freq'] = freq[index]
    stat = {
        'all_cpu_load': all_cpu_load,
        "per_cpu_load": per_cpu_load
    }
    return stat

def mem_stat(pid) -> dict:
    mems = {}
    with open('/proc/meminfo', 'r') as f:
        res = f.readlines()
        for line in res:
            fields = line.split()
            # MB
            mems[fields[0]] = int(fields[1]) / 1024
    data = {
        "Cached": mems["Cached:"],
        "AnonPages": mems["AnonPages:"],
        "Shmem": mems["Shmem:"],
        "Slab": mems["Slab:"],
        "SReclaimable": mems["SReclaimable:"],
        "SUnreclaim": mems["SUnreclaim:"],
        "MemFree": mems["MemFree:"],
        "Buffers": mems["Buffers:"],
    }
    if "KReclaimable" in mems:
        data["KReclaimable"] = mems["KReclaimable:"],
    return data

# PERF_CMD = "perf stat --per-core -v -a -e page-faults "
PERF_CMD = "perf record -e page-faults "

def perf_stat(pid, interval) -> dict:
    sh="perf stat -e page-faults -p {} -j -a sleep {}".format(pid, interval)
    data = subprocess.check_output(sh.split(" "))
    return json.loads(data)

def run_shell(sh):
    sh = get_sh_path(sh)
    # sh = PERF_CMD + get_sh_path(sh)
    data = subprocess.check_output(sh.split(" "))
    data = data.decode()
    print(data)
    return data

def get_sh_path(str):
    return sys.path[0]+'/sh/'+str


def start_trace(pid, function_names):
    print("Setting ftrace parameters ...\n")
    os.system("rm -f log")
    print("Disabling trace ...\n")
    os.system("echo 0 > /sys/kernel/debug/tracing/tracing_on")
    print("Clearing trace file ...\n")
    os.system("> /sys/kernel/debug/tracing/trace")
    print("Selecting current tracer ...")
    os.system("echo function_graph | tee /sys/kernel/debug/tracing/current_tracer")
    print("Selecting ftrace filter ...")
    os.system(f"echo | tee /sys/kernel/debug/tracing/set_ftrace_filter")
    for f in function_names:
        os.system(f"echo {f} >> /sys/kernel/debug/tracing/set_ftrace_filter")
    print("Enabling trace for forked pidsi ...")
    os.system("echo 1 > /sys/kernel/debug/tracing/options/function-fork")
    print("Increasing trace buffer size ...")
    os.system("echo 512000 > /sys/kernel/debug/tracing/buffer_size_kb")
    print("Configuring ftrace PID ...")
    os.system(f"echo {pid} > /sys/kernel/debug/tracing/set_ftrace_pid")
    print("Enabling tracing ...")
    os.system("echo 1 > /sys/kernel/debug/tracing/tracing_on")
    print("ftrace configured. Executing the workload...")
    

def end_trace(function_names):
    print("dumping and clearing trace")
    os.system("echo 0 > /sys/kernel/debug/tracing/tracing_on")
    for f in function_names:
        os.system("tail -n+5 /sys/kernel/debug/tracing/trace >> log")
        os.system(f"sed 's/^.......//' log > tmp; rm -r log;\
                cat tmp | grep {f} > log; rm -f tmp")
        print(f"Status for {f}")
        os.system("total=$(awk '{sum+=$1;n++} END { if(n>0) print(sum)}' log);\
                    echo Total Page Fault Time: $total us")
        os.system("total=$(awk '{n++} END { if(n>0) print(n)}' log);\
                    echo Total Page Fault Num: $total")
        os.system("avg=$(awk '{sum+=$1;n++} END { if(n>0) print(sum/n)}' log);\
                    echo Average Page Fault Time: $avg us; rm -f log")
    os.system("> /sys/kernel/debug/tracing/trace")
    print("ftrace parameters cleared successfully...")
    os.system("echo 1408 > /sys/kernel/debug/tracing/buffer_size_kb")
    os.system("echo 1 > /sys/kernel/debug/tracing/tracing_on")

def get_cur_time():
    return time.strftime("%H:%M:%S", time.localtime())
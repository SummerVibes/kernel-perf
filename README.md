# kernel-perf-test

内核性能测试框架，可以轻松集成测试项目并将测试结果以及性能监控信息直观的展示出来，目前支持内存、CPU 各项指标的监控

# 使用方式

1. 运行 prepare.sh 安装必要的依赖
2. 编辑 src/perf.py 自定义要进行哪些测试项目
3. 运行 run.sh 开始测试，测试结果会被写入 perf-%d-%H-%M-%S.json 文件
4. 上传 json 文件到 [perf-viewer](https://newgh.smartx.com/kernel/perf-viewer), 查看解析结果, 当前运行在一台虚拟机上 http://192.168.31.45:8000/

# 测试项目

目前支持以下测试项目

| Item           | Tool     | Env    |
| -------------- | -------- | ------ |
| 内存性能测试   | sysbench | docker |
| CPU 性能测试   | sysbench | docker |
| mysql 性能测试 | sysbench | docker |
| 内核编译测试   | time     | docker |
| 网络性能测试   | iperf3   | host   |

为了保持测试环境的一致性以及避免过多的影响测试环境，使用 docker 进行部分性能测试，基于 openeuler-kernel-build 容器

关于在 docker 中跑性能测试是否会有不一致的问题，通过 sysbench 测试，发现CPU 和内存性能相差无几，io 性能差距较大。测试时 host 使用 `cgexec --sticky -g cpuset:/` 避免 cgroup 的限制，host 和 docker 使用同样的命令，线程数设置为 CPU 核数。

| Item           | Docker             | Host               |
| -------------- | ------------------ | ------------------ |
| 内存性能测试   | 11916.84 MiB/s     | 11807.22 MiB/s     |
| CPU 性能测试   | 115875.97 events/s | 115377.90 events/s |
| IO random read | 17.13 MiB/s        | 9.47 MiB/s         |
| IO random read | 11.42 MiB/s        | 6.31 MiB/s         |

# 自定义测试项目

可以按照如下流程自定义一个测试项

1. 编写运行测试程序的脚本，可以参考 src/sh 目录下的脚本，如果测试程序需要预先准备或是运行后需要清理线程，可以参考 src/sh/mysql
2. 创建一个 PerfTask，可以直接复制 task/mysql.py 作为模版进行修改
3. 在 perf.py 中加入一个 TaskRunner，默认 monior interval 是 1，可以根据需要修改
4. 运行 run.sh，脚本会依次运行 PerfTask
